import sys
import time
from pathlib import Path

from openai import OpenAI

openai = OpenAI()

SECONDS = 12  # Duration of the video in seconds (4, 8, or 12)
SORA_MODELS = ["sora-2", "sora-2-pro"]

# Create video generation job
# Parameters:
#   model: "sora-2" (fast, 720p) or "sora-2-pro" (high quality, 1024p+)
#   prompt: Detailed description (include shot type, subject, action, setting, lighting)
#   size: Resolution like "1280x720" (landscape), "720x1280" (portrait), "1024x1024" (square)
#   seconds: Duration as "4", "8", or "12" (default is "8")
#   seed: Optional integer for reproducibility
#   input_reference: Optional starting image file (JPEG, PNG, WebP)
video = openai.videos.create(
    model="sora-2-pro",  # Models: "sora-2" ($3/10s) or "sora-2-pro" ($5/10s)
    prompt="Medium shot of a construction site. A construction worker in an orange safety vest and white hard hat walks under scaffolding while looking at his phone, distracted. As he passes underneath, a tool bag falls from the scaffold above and strikes near him, causing him to stumble and fall to the ground. Other workers in the background rush to help. Overcast daylight, industrial setting with construction equipment visible. Camera remains steady to capture the accident sequence for safety training purposes.",
    seconds=str(SECONDS),  # Must be a string: "4", "8", or "12"
    size="1280x720",
)

print("Video generation started:", video)

# Poll for completion with progress bar
progress = getattr(video, "progress", 0)
bar_length = 30

while video.status in ("in_progress", "queued"):
    # Refresh status
    video = openai.videos.retrieve(video.id)
    progress = getattr(video, "progress", 0)

    filled_length = int((progress / 100) * bar_length)
    bar = "=" * filled_length + "-" * (bar_length - filled_length)
    status_text = "Queued" if video.status == "queued" else "Processing"

    sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
    sys.stdout.flush()
    time.sleep(2)

# Move to next line after progress loop
sys.stdout.write("\n")

if video.status == "failed":
    message = getattr(getattr(video, "error", None), "message", "Video generation failed")
    print(message)
    sys.exit(1)

print("Video generation completed:", video)
print("Downloading video content...")

# Create .bin directory if it doesn't exist
bin_dir = Path(".bin")
bin_dir.mkdir(exist_ok=True)

# Use the video ID as unique identifier for the filename
video_filename = f"{video.id}.mp4"
video_path = bin_dir / video_filename

content = openai.videos.download_content(video.id, variant="video")
content.write_to_file(str(video_path))

print(f"Wrote {video_path}")
