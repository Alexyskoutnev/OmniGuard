import dataclasses
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import ClassVar

from google import genai
from google.genai import types

from domain.event import Event

VIDEO_TRANSCRIPTION_PROMPT: str = """You are a construction site safety expert analyzing video footage for hazards.

Analyze this construction site video and identify all safety hazards present. For each hazard:
1. Identify the specific hazard type from the available categories
2. Provide a clear description of what you observe
3. Assess the risk level (CRITICAL, HIGH, MEDIUM, LOW)
4. Recommend specific actions to mitigate the hazard

Return your analysis as a JSON object matching this schema:

{
  "video_id": string,
  "location_description": string,
  "hazards": [
    {
      "hazard_type": enum[
        "Fall Hazard (Height)",
        "Trip/Slip Hazard (Ground)",
        "Unsecured Working Platform",
        "Struck-by (Moving Equipment/Vehicle)",
        "Crush/Proximity Hazard (Blind Spot)",
        "Dropped Object Hazard",
        "Equipment-Equipment Collision Risk",
        "PPE Violation (Missing/Incorrect)",
        "Electrical Hazard (Exposed Wire/Damage)",
        "Lockout/Tagout Violation",
        "Improper Lifting/Rigging",
        "Pressurized Gas/Cylinder Hazard",
        "Fire/Explosion Hazard",
        "Confined Space Entry Violation",
        "Chemical Exposure/Spill",
        "Excessive Noise Exposure",
        "Heat/Cold Stress",
        "Improper Material Storage/Stacking",
        "Improper Tool Use",
        "Trench/Excavation Cave-in Risk",
        "Unguarded Floor/Wall Opening",
        "Unsafe Worker Behavior/Distraction",
        "Other Safety Concern"
      ],
      "description": string,
      "risk_level": enum["CRITICAL", "HIGH", "MEDIUM", "LOW"],
      "recommended_actions": array[string]
    }
  ]
}

Example:
{
  "video_id": "video_001",
  "location_description": "Scaffolding area on third floor of construction site",
  "hazards": [
    {
      "hazard_type": "PPE Violation (Missing/Incorrect)",
      "description": "Worker operating without hard hat near overhead work",
      "risk_level": "HIGH",
      "recommended_actions": [
        "Require all workers to wear proper PPE",
        "Conduct safety briefing",
        "Post PPE requirement signage"
      ]
    }
  ]
}

If no hazards are detected, return an empty hazards array."""


@dataclasses.dataclass
class VideoTranscriptionConfig:
    model: str = "models/gemini-2.5-flash"
    temperature: float = 0.1
    max_retries: int = 3
    max_workers: int = dataclasses.field(default_factory=lambda: max(1, os.cpu_count() - 1))


@dataclasses.dataclass
class VideoTranscription:
    client: genai.Client
    config: VideoTranscriptionConfig = dataclasses.field(default_factory=VideoTranscriptionConfig)
    thread_executor: ThreadPoolExecutor | None = None
    VIDEO_MIME_TYPE: ClassVar[str] = "video/mp4"

    def __post_init__(self):
        if self.thread_executor is None:
            self.thread_executor = ThreadPoolExecutor(max_workers=self.config.max_workers)

    def _create_video_content(self, video_data: bytes) -> types.Content:
        return types.Content(
            parts=[
                types.Part(inline_data=types.Blob(data=video_data, mime_type=self.VIDEO_MIME_TYPE)),
                types.Part(text=VIDEO_TRANSCRIPTION_PROMPT),
            ]
        )

    def _create_generation_config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=self.config.temperature,
        )

    def _process(self, element: bytes, video_id: str | None = None) -> Event:
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                logging.info(f"Processing video (attempt {attempt + 1}/{self.config.max_retries})")

                response = self.client.models.generate_content(
                    model=self.config.model,
                    contents=self._create_video_content(element),
                    config=self._create_generation_config(),
                )

                response_text = response.text
                data = json.loads(response_text)
                event = Event.model_validate(data)

                # Override video_id if provided
                if video_id:
                    event.video_id = video_id

                logging.info(f"Successfully processed video. Found {len(event.hazards)} hazards")
                return event

            except json.JSONDecodeError as e:
                last_error = e
                logging.error(f"Failed to parse JSON response: {e}")

            except Exception as e:
                last_error = e
                logging.error(f"Error processing video: {e}")

            if attempt < self.config.max_retries - 1:
                logging.info(f"Retrying... ({attempt + 2}/{self.config.max_retries})")

        raise Exception(
            f"Failed to process video after {self.config.max_retries} attempts"
        ) from last_error

    def process(self, videos: list[tuple[bytes, str]]) -> list[Event]:
        logging.info(f"Processing {len(videos)} videos with {self.config.max_workers} workers")

        futures = []
        with self.thread_executor as executor:
            for _idx, (video_data, video_id) in enumerate(videos):
                futures.append(executor.submit(self._process, video_data, video_id=video_id))

        results = []
        for idx, future in enumerate(futures):
            try:
                event = future.result()
                results.append(event)
            except Exception as e:
                logging.error(f"Failed to process video {idx}: {e}")

        logging.info(f"Successfully processed {len(results)}/{len(videos)} videos")
        return results


def main():
    logging.basicConfig(level=logging.INFO)
    api_key = os.getenv("GEMINI_API_KEY")
    video_dir = ".bin/videos"

    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(".mp4")]

    logging.info(f"Found {len(video_files)} videos to process")

    client = genai.Client(api_key=api_key)
    service = VideoTranscription(client=client)

    input = []
    for idx, video_file in enumerate(video_files, 1):
        filename = os.path.basename(video_file).replace(".mp4", "")
        logging.info(f"[{idx}/{len(video_files)}] Processing: {filename}")

        with open(video_file, "rb") as f:
            video_bytes = f.read()

        input.append((video_bytes, filename))

    events = service.process(input)
    os.makedirs(".bin/events", exist_ok=True)

    for event in events:
        # save as json
        output_file = os.path.join(".bin/events", f"{event.video_id}.json")
        with open(output_file, "w") as f:
            f.write(event.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
