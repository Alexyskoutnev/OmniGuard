import dataclasses
import hashlib
import logging
import os
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
)

DATASET_VIDEOS_DIR = Path(__file__).parent.parent / ".bin" / "videos"
os.makedirs(DATASET_VIDEOS_DIR, exist_ok=True)


VALID_DURATIONS = {
    "sora-2": [4, 8, 12],
    "sora-2-pro": [4, 8, 12],
}


@dataclasses.dataclass
class VideoConfig:
    model: str = "sora-2-pro"  # "sora-2" or "sora-2-pro"
    seconds: int = 12  # sora-2: [4, 8, 12], sora-2-pro: [4, 8, 12]
    size: str = "1280x720"
    # seed: int | None = None  # Not supported by Sora API yet

    def __post_init__(self):
        if self.model not in VALID_DURATIONS:
            msg = f"Invalid model '{self.model}'. Must be one of: {list(VALID_DURATIONS.keys())}"
            raise ValueError(msg)

        valid_seconds = VALID_DURATIONS[self.model]
        if self.seconds not in valid_seconds:
            msg = f"Invalid seconds '{self.seconds}' for model '{self.model}'. Must be one of: {valid_seconds}"
            raise ValueError(msg)


@dataclasses.dataclass
class VideoResult:
    prompt: str
    video_id: uuid.UUID
    status: str = "pending"  # pending, completed, failed, error
    video_bytes: bytes | None = None
    video_path: Path | None = None
    error_message: str | None = None


@dataclasses.dataclass
class VideoDatasetGenerator:
    config: VideoConfig = dataclasses.field(default_factory=VideoConfig)
    output_dir: Path = DATASET_VIDEOS_DIR
    max_workers: int = os.cpu_count() - 1
    poll_interval: int = 1
    client: OpenAI = dataclasses.field(default_factory=lambda: OpenAI())

    def __post_init__(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, prompt: str, video_id: str) -> str:
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{prompt_hash}_{video_id}.mp4"

    def _create_video_job(self, prompt: str) -> Any:
        params = {
            "model": self.config.model,
            "prompt": prompt,
            "seconds": str(self.config.seconds),
            "size": self.config.size,
        }
        return self.client.videos.create(**params)

    def _poll_video(self, video_id: uuid.UUID, unique_id: uuid.UUID) -> Any:
        bar_length = 40
        last_progress = 0

        while True:
            video = self.client.videos.retrieve(str(video_id))

            if video.status not in ("in_progress", "queued"):
                # Clear progress bar on completion
                sys.stdout.write(f"\r[{unique_id}] {'=' * bar_length} 100%\n")
                sys.stdout.flush()
                return video

            # Get progress percentage
            progress = getattr(video, "progress", 0)

            # Only update if progress changed
            if progress != last_progress:
                filled = int((progress / 100) * bar_length)
                bar = "=" * filled + "-" * (bar_length - filled)
                status = "Queued" if video.status == "queued" else "Processing"

                sys.stdout.write(f"\r[{unique_id}] {status}: [{bar}] {progress:.1f}%")
                sys.stdout.flush()
                last_progress = progress

            time.sleep(self.poll_interval)

    def _download_video(self, video_id: uuid.UUID, filename: str) -> Path:
        video_path = self.output_dir / filename
        content = self.client.videos.download_content(str(video_id), variant="video")
        content.write_to_file(str(video_path))
        return video_path

    def _generate_single(self, prompt: str) -> VideoResult:
        unique_id = uuid.uuid4()

        result = VideoResult(prompt=prompt, video_id=unique_id)

        try:
            logger.info(f"[{unique_id}] Creating video job: {prompt[:60]}...")
            video = self._create_video_job(prompt)
            api_video_id = video.id
            logger.info(f"[{unique_id}] API video ID: {api_video_id}")

            # Poll with progress bar
            video = self._poll_video(api_video_id, unique_id)

            if video.status == "failed":
                result.status = "failed"
                result.error_message = getattr(
                    getattr(video, "error", None), "message", "Video generation failed"
                )
                logger.error(f"[{unique_id}] Failed: {result.error_message}")
                return result

            logger.info(f"[{unique_id}] Completed, downloading...")
            filename = self._generate_filename(prompt, str(api_video_id))
            video_path = self._download_video(api_video_id, filename)
            result.video_path = video_path
            result.video_bytes = video_path.read_bytes()
            result.status = "completed"
            logger.info(f"[{unique_id}] Saved: {video_path}")

        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            logger.error(f"[{unique_id}] Error: {e}")

        return result

    def _process(self, prompts: list[str]) -> list[VideoResult]:
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_prompt = {
                executor.submit(self._generate_single, prompt): prompt for prompt in prompts
            }

            completed_count = 0
            for future in as_completed(future_to_prompt):
                prompt = future_to_prompt[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed_count += 1
                    logger.info(f"Progress: {completed_count}/{len(prompts)} videos processed")
                except Exception as e:
                    logger.error(f"Exception for prompt '{prompt[:60]}...': {e}")
                    results.append(
                        VideoResult(
                            prompt=prompt,
                            video_id=uuid.uuid4(),
                            status="error",
                            error_message=str(e),
                        )
                    )

        return results

    def process(self, prompts: list[str]) -> list[VideoResult]:
        start_time = time.time()
        results = self._process(prompts)
        elapsed = time.time() - start_time
        successful = sum(1 for r in results if r.status == "completed")
        failed = len(results) - successful
        logger.info(f"Batch completed in {elapsed:.1f}s")
        logger.info(f"Successful: {successful}/{len(prompts)}, Failed: {failed}/{len(prompts)}")
        return results


if __name__ == "__main__":
    from safety_prompts import get_all_prompts

    prompts = get_all_prompts()
    generator = VideoDatasetGenerator(
        config=VideoConfig(),
        max_workers=10,
        poll_interval=2,
    )
    generator.process(prompts)
