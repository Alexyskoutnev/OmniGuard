# Safety Agent Dataset Generator

Generate construction safety training videos using OpenAI's Sora API with parallel processing and real-time progress tracking.

## Quick Start

```python
from dataset.video_dataset_generator import VideoDatasetGenerator, VideoConfig
from dataset.safety_prompts import get_all_prompts

# Generate all 25 safety scenarios
config = VideoConfig(model="sora-2-pro", seconds=12)
generator = VideoDatasetGenerator(config=config, max_workers=2)
results = generator.process(get_all_prompts())
```

## Installation

```bash
pip install openai
export OPENAI_API_KEY='your-api-key'
```

## Features

- Parallel video generation with configurable workers
- Real-time progress bars for each video
- 25 early-detection safety scenarios (falling objects, electrical hazards, excavation, equipment collisions, fall protection, etc.)
- Automatic file naming and metadata tracking

## Configuration

```python
VideoConfig(
    model="sora-2-pro",    # or "sora-2"
    seconds=12,            # sora-2: [4,8,12], sora-2-pro: [4,8,12]
    size="1280x720"
)
```

Videos saved to `.bin/videos/`
