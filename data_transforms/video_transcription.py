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

Analyze this construction site video and assess the safety status. For any incidents detected:
1. Determine the overall safety status (SAFE, LOW, MEDIUM, HIGH, EXTREME)
2. Describe the scene and what you observe
3. Identify the incident type and estimate the probability of occurrence
4. Provide a specific safety response action

Return your analysis as a JSON object matching this schema:

{
  "video_id": string,
  "safety_status": enum["SAFE", "LOW", "MEDIUM", "HIGH", "EXTREME"],
  "scene_description": string,
  "predictions": {
    "probability": float (0.0 to 1.0),
    "incident_type": enum[
      "Fall Hazard (Height)",
      "Trip/Slip Hazard (Ground)",
      "Unsecured Working Platform",
      "Struck-by (Moving Equipment/Vehicle)",
      "Crush/Proximity Hazard (Blind Spot)",
      "Caught-in/Caught-between Machinery",
      "Dropped Object Hazard",
      "Equipment-Equipment Collision Risk",
      "Equipment Instability/Tip-over Risk",
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
      "Laceration/Severe Bleeding",
      "Muscle Strain/Sprain Injury",
      "Eye Injury/Foreign Object",
      "Burn/Thermal Injury",
      "Call 911 - Emergency Services Required",
      "Fire Department Required",
      "Medical Emergency - First Aid/Ambulance",
      "Evacuation Required",
      "Active Fire/Smoke",
      "Person Down/Injured",
      "Hazmat/Chemical Incident Response",
      "Structural Collapse/Damage",
      "Unsafe Worker Behavior/Distraction",
      "Other Safety Concern",
      "No Hazard Detected"
    ]
  },
  "safety_response": string
}

Example:
{
  "video_id": "video_001",
  "safety_status": "HIGH",
  "scene_description": "Scaffolding area on third floor of construction site with worker operating without proper head protection near overhead work",
  "predictions": {
    "probability": 0.85,
    "incident_type": "PPE Violation (Missing/Incorrect)"
  },
  "safety_response": "Require all workers to wear proper PPE including hard hats. Conduct immediate safety briefing and post PPE requirement signage in visible areas."
}

Guidelines:
- SAFE: Normal operations with no hazards detected
- LOW: Minor safety concern, no immediate risk
- MEDIUM: Potential hazard that needs attention soon
- HIGH: Serious hazard requiring immediate attention
- EXTREME: Life-threatening situation requiring emergency response
- Probability should reflect likelihood of incident: 0.0-0.3 (low), 0.4-0.6 (medium), 0.7-1.0 (high)"""


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

                logging.info(
                    f"Successfully processed video. Status: {event.safety_status}, Incident: {event.predictions.incident_type}"
                )
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
            for video_data, video_id in videos:
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
