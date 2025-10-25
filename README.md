# Construction Safety Video Analysis with NVIDIA OmniVinci

A complete pipeline for training vision-language models to analyze construction site videos for safety violations, accident prediction, and remediation recommendations.

## Project Overview

This project fine-tunes NVIDIA's OmniVinci multimodal AI model to:
- Analyze construction site videos for safety violations
- Predict potential accidents based on observed conditions
- Provide specific remediation recommendations
- Generate structured safety reports

## Features

- **Multimodal Analysis**: Processes both video and audio from construction sites
- **Comprehensive Safety Assessment**: Evaluates PPE compliance, equipment safety, environmental hazards
- **Accident Prediction**: Predicts potential incidents with probability estimates
- **Actionable Remediation**: Provides specific, prioritized safety recommendations
- **Efficient Training**: Uses LoRA/QLoRA for memory-efficient fine-tuning on H100 GPUs

## Project Structure

```
aitx-hack/
├── config.py                      # Configuration settings
├── src/
│   ├── train/
│   │   ├── train.py               # LoRA fine-tuning pipeline
│   │   ├── inference.py           # Safety analysis inference
│   │   ├── evaluate.py            # Model evaluation and metrics
│   │   └── merge.py               # Model merging utilities
│   ├── data/
│   │   ├── dataset.py             # Dataset handling
│   │   ├── video_preprocessing.py # Video preprocessing pipeline
│   │   ├── safety_annotation_schema.py # Safety annotation structures
│   │   └── annotation_templates.py # Training data generation
│   └── utils/
│       ├── model_utils.py         # Model management utilities
│       └── analyze_videos.py      # Video analysis utilities
├── finetune/
│   ├── model/omnivinci/          # Local OmniVinci model
│   └── src/dataset/              # Training videos
└── outputs/                      # Generated outputs and results
```

## Setup Instructions

### 1. Environment Setup

```bash
# Install dependencies using uv
uv sync

# For GPU support (Linux), also install:
# uv sync --extra gpu
```

### 2. Model Preparation

The OmniVinci model should be available in `finetune/model/omnivinci/`. The project is configured to use the local model path.

### 3. Dataset Analysis

```bash
# Analyze your video dataset
uv run python src/utils/analyze_videos.py

# Preprocess videos for training
uv run python src/data/video_preprocessing.py
```

### 4. Annotation Schema

```bash
# Generate safety annotation schema and examples
uv run python src/data/safety_annotation_schema.py

# Create training dataset templates
uv run python src/data/annotation_templates.py
```

## Training Pipeline

### Fine-tuning with LoRA

```bash
# Run fine-tuning (requires OmniVinci model to be downloaded)
uv run python src/train/train.py
```

### Model Evaluation

```bash
# Evaluate model performance
uv run python src/train/evaluate.py
```

### Model Merging

```bash
# Merge LoRA weights with base model for standalone deployment
uv run python src/train/merge.py
```

## Safety Analysis Pipeline

### Inference

```bash
# Run safety analysis on all videos
uv run python src/train/inference.py
```

### Analysis Types

1. **Comprehensive Analysis**: Full safety assessment with violations, predictions, and remediation
2. **Accident Prediction**: Focus on potential incident forecasting
3. **Remediation Planning**: Specific safety improvement recommendations

## Key Commands

| Command | Description |
|---------|-------------|
| `uv run python src/train/train.py` | Fine-tune OmniVinci with LoRA |
| `uv run python src/train/inference.py` | Run safety analysis inference |
| `uv run python src/train/evaluate.py` | Evaluate model performance |
| `uv run python src/train/merge.py` | Merge LoRA weights with base model |

## Technical Details

### Video Processing
- **Input**: MP4 videos up to 30 seconds
- **Frame Sampling**: 4 FPS (up to 128 frames)
- **Resolution**: 224x224 for model input
- **Audio**: Optional audio processing with 16kHz sampling

### Model Architecture
- **Base Model**: NVIDIA OmniVinci multimodal LLM
- **Fine-tuning**: LoRA with rank 16
- **Target Modules**: Attention layers (q_proj, v_proj, k_proj, o_proj)
- **Memory Optimization**: FP16, gradient checkpointing

### Hardware Requirements
- **GPU**: NVIDIA H100 (80GB) recommended
- **Memory**: ~60GB for fine-tuning, ~20GB for inference
- **Storage**: 50GB+ for model and data

## Usage Examples

### Basic Training

```python
# Training
from src.train.train import OmniVinciTrainer, TrainingConfig

config = TrainingConfig()
trainer = OmniVinciTrainer(config)
trainer.train()
```

### Safety Analysis

```python
# Inference
from src.train.inference import SafetyInferenceEngine

inference = SafetyInferenceEngine(use_finetuned=True)
result = inference.analyze_video("construction_video.mp4", "comprehensive")
print(result.prediction)
```

### Model Evaluation

```python
# Evaluation
from src.train.evaluate import SafetyAnalysisEvaluator

evaluator = SafetyAnalysisEvaluator()
results = evaluator.compare_models()
```

## File Outputs

The system generates several output files:

- `outputs/video_analysis.json`: Video metadata and analysis
- `outputs/safety_annotation_schema.json`: Complete annotation schema
- `outputs/training_dataset.json`: Formatted training conversations
- `outputs/finetuned_model/`: Fine-tuned model weights
- `outputs/merged_model_*/`: Standalone merged models
- `outputs/safety_analysis_results_*.json`: Inference results
- `outputs/evaluation_results_*.json`: Model performance metrics

## Current Status

✅ **Completed Components:**
- Modular project structure with src/train organization
- Environment setup with uv package management
- Video analysis and preprocessing pipeline
- Comprehensive safety annotation schema
- Training data generation with OmniVinci format
- LoRA fine-tuning pipeline implementation
- Multi-modal inference pipeline for safety analysis
- Model evaluation and comparison framework
- Model merging utilities for deployment

⏳ **Pending:**
- OmniVinci model download completion
- Model testing and validation
- Fine-tuning execution
- Performance evaluation

## Next Steps

1. **Test Model Loading**: Once OmniVinci download completes, run model tests
2. **Execute Training**: Run `uv run python src/train/train.py`
3. **Evaluate Performance**: Run `uv run python src/train/evaluate.py`
4. **Deploy Pipeline**: Use `uv run python src/train/merge.py` for standalone model

This project provides a complete, modular framework for construction safety video analysis with clear separation of concerns between training, inference, evaluation, and deployment components.