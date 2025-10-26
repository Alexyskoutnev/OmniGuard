import json
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from google import genai
from google.genai import types

from agent.safety_agents import create_runner, run_agent_system
from domain.event import Event

GEMINI_MODEL_VERSION = "gemini-2.5-pro"
VIDEO_SAFETY_PROMPT: str = """Analyze this construction site or workplace safety video and identify any safety hazards or incidents.

Provide a detailed analysis including:
1. Scene description: What is happening in the video
2. Safety status: SAFE, LOW, MEDIUM, HIGH, or EXTREME based on severity
3. Incident type: Choose the most relevant incident type from the available categories
4. Probability: How likely (0.0 to 1.0) this incident will result in injury or damage
5. Safety response: Recommended immediate actions to address the hazard

Focus on:
- Worker safety and PPE compliance
- Equipment hazards and moving machinery
- Fall hazards and height work
- Fire, electrical, and environmental hazards
- Medical emergencies or injured workers
- Unsafe behaviors or working conditions

Respond with a JSON object matching this structure."""


def run_video_model(video_bytes: bytes, video_id: str) -> str:
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")

    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
        model=GEMINI_MODEL_VERSION,
        contents=types.Content(
            parts=[
                types.Part(inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")),
                types.Part(text=VIDEO_SAFETY_PROMPT),
            ]
        ),
        config=types.GenerateContentConfig(
            response_mime_type="application/json", response_schema=Event
        ),
    )
    result_dict = json.loads(response.text)
    result_dict["video_id"] = video_id
    logging.debug(f"Video model result: {result_dict}")
    event = Event(**result_dict)
    return str(event.model_dump_json())


def pipeline(video_bytes: bytes, video_id: str = "", verbose: bool = True) -> str:
    event_description = run_video_model(video_bytes, video_id or "unknown_video")
    # Run the safety agent system
    runner = create_runner(verbose=verbose)
    result = run_agent_system(event_description, runner)
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    video_path = ".bin/videos/20251025_161628_d5957a56_video_68fd3c9a73bc8198b786a1d8e7b8874309f1b0907b4a562b.mp4"

    with open(video_path, "rb") as f:
        video_bytes = f.read()

    video_id = Path(video_path).stem
    event = run_video_model(video_bytes, video_id)
    output = pipeline(video_bytes=video_bytes, video_id=video_id, verbose=True)

    print(output)
