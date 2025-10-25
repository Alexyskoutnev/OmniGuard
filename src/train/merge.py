"""
Model merging utilities for OmniVinci fine-tuned models
"""

import torch
from pathlib import Path
from typing import Optional
import logging
from datetime import datetime

from transformers import AutoProcessor, AutoModel, AutoConfig
from peft import PeftModel

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import OMNIVINCI_MODEL_PATH, OUTPUT_DIR

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMerger:
    """Utility class for merging LoRA weights with base model."""

    def __init__(self, base_model_path: str = None):
        self.base_model_path = base_model_path or OMNIVINCI_MODEL_PATH
        self.finetuned_path = OUTPUT_DIR / "finetuned_model" / "final_model"

    def merge_lora_weights(self, output_path: str = None) -> Path:
        """
        Merge LoRA adapter weights with the base model to create a standalone model.

        Args:
            output_path: Path to save the merged model. If None, uses default path.

        Returns:
            Path to the merged model directory.
        """

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"merged_model_{timestamp}"

        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting model merge process")
        logger.info(f"Base model: {self.base_model_path}")
        logger.info(f"LoRA adapter: {self.finetuned_path}")
        logger.info(f"Output path: {output_path}")

        try:
            # Check if LoRA adapter exists
            if not self.finetuned_path.exists():
                raise FileNotFoundError(f"LoRA adapter not found at {self.finetuned_path}")

            # Load base model
            logger.info("Loading base model...")
            base_model = AutoModel.from_pretrained(
                self.base_model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16,
                device_map="auto"
            )

            # Load LoRA adapter
            logger.info("Loading LoRA adapter...")
            peft_model = PeftModel.from_pretrained(
                base_model,
                str(self.finetuned_path),
                torch_dtype=torch.float16
            )

            # Merge weights
            logger.info("Merging LoRA weights with base model...")
            merged_model = peft_model.merge_and_unload()

            # Save merged model
            logger.info(f"Saving merged model to {output_path}")
            merged_model.save_pretrained(
                str(output_path),
                torch_dtype=torch.float16,
                safe_serialization=True
            )

            # Copy processor and other necessary files
            logger.info("Copying processor and configuration files...")
            processor = AutoProcessor.from_pretrained(
                self.base_model_path,
                trust_remote_code=True
            )
            processor.save_pretrained(str(output_path))

            # Copy configuration
            config = AutoConfig.from_pretrained(
                self.base_model_path,
                trust_remote_code=True
            )
            config.save_pretrained(str(output_path))

            # Copy any custom code files from base model
            self._copy_custom_files(Path(self.base_model_path), output_path)

            logger.info("Model merge completed successfully!")
            return output_path

        except Exception as e:
            logger.error(f"Model merge failed: {e}")
            raise

    def _copy_custom_files(self, source_dir: Path, target_dir: Path):
        """Copy custom Python files and other necessary files from source to target."""

        # Files that typically need to be copied for custom models
        files_to_copy = [
            "*.py",  # All Python files
            "*.jinja",  # Template files
            "*.sh",  # Shell scripts
            "*.md",  # Documentation
            "*.txt",  # Text files
        ]

        for pattern in files_to_copy:
            for file_path in source_dir.glob(pattern):
                if file_path.is_file():
                    target_file = target_dir / file_path.name
                    try:
                        target_file.write_bytes(file_path.read_bytes())
                        logger.debug(f"Copied {file_path.name}")
                    except Exception as e:
                        logger.warning(f"Failed to copy {file_path.name}: {e}")

        # Copy subdirectories that might contain custom code
        important_dirs = ["transformers", "vision_tower", "sound_tower", "llm"]
        for dir_name in important_dirs:
            source_subdir = source_dir / dir_name
            if source_subdir.exists() and source_subdir.is_dir():
                target_subdir = target_dir / dir_name
                target_subdir.mkdir(exist_ok=True)
                self._copy_directory_contents(source_subdir, target_subdir)

    def _copy_directory_contents(self, source_dir: Path, target_dir: Path):
        """Recursively copy directory contents."""

        for item in source_dir.iterdir():
            target_item = target_dir / item.name
            try:
                if item.is_file():
                    target_item.write_bytes(item.read_bytes())
                elif item.is_dir():
                    target_item.mkdir(exist_ok=True)
                    self._copy_directory_contents(item, target_item)
            except Exception as e:
                logger.warning(f"Failed to copy {item}: {e}")

    def validate_merged_model(self, merged_model_path: Path) -> bool:
        """
        Validate that the merged model can be loaded and used for inference.

        Args:
            merged_model_path: Path to the merged model directory.

        Returns:
            True if model validation passes, False otherwise.
        """

        logger.info(f"Validating merged model at {merged_model_path}")

        try:
            # Try to load the merged model
            model = AutoModel.from_pretrained(
                str(merged_model_path),
                trust_remote_code=True,
                torch_dtype=torch.float16,
                device_map="auto"
            )

            processor = AutoProcessor.from_pretrained(
                str(merged_model_path),
                trust_remote_code=True
            )

            logger.info("Model and processor loaded successfully")

            # Test basic functionality
            test_prompt = "Analyze this construction site for safety concerns."
            conversation = [{
                "role": "user",
                "content": [{"type": "text", "text": test_prompt}]
            }]

            text = processor.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )

            inputs = processor([text])

            # Test generation (small output to validate)
            with torch.no_grad():
                output_ids = model.generate(
                    input_ids=inputs.input_ids,
                    max_new_tokens=10,
                    do_sample=False
                )

            response = processor.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
            logger.info("Model generation test passed")

            return True

        except Exception as e:
            logger.error(f"Model validation failed: {e}")
            return False

    def create_model_card(self, merged_model_path: Path):
        """Create a model card for the merged model."""

        model_card_content = f"""
# Construction Safety Analysis Model

This model is a fine-tuned version of NVIDIA OmniVinci specialized for construction safety video analysis.

## Model Description

- **Base Model**: NVIDIA OmniVinci
- **Fine-tuning Method**: LoRA (Low-Rank Adaptation)
- **Task**: Construction safety analysis, accident prediction, and remediation recommendations
- **Training Date**: {datetime.now().strftime('%Y-%m-%d')}

## Capabilities

- Analyze construction site videos for safety violations
- Detect PPE compliance issues
- Predict potential accidents based on observed conditions
- Provide specific remediation recommendations
- Process both video and audio inputs

## Usage

```python
from transformers import AutoProcessor, AutoModel

model = AutoModel.from_pretrained(
    "{merged_model_path.name}",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

processor = AutoProcessor.from_pretrained(
    "{merged_model_path.name}",
    trust_remote_code=True
)

# Analyze a construction video
conversation = [{{
    "role": "user",
    "content": [
        {{"type": "video", "video": "construction_video.mp4"}},
        {{"type": "text", "text": "Analyze this construction site for safety concerns."}}
    ]
}}]

text = processor.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
inputs = processor([text])

output_ids = model.generate(
    input_ids=inputs.input_ids,
    media=getattr(inputs, 'media', None),
    media_config=getattr(inputs, 'media_config', None),
    max_new_tokens=512
)

response = processor.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
```

## Safety Analysis Format

The model provides structured safety analysis including:
- Overall safety status (Low/Medium/High/Critical)
- Specific safety violations identified
- Risk assessment and probability estimates
- Actionable remediation recommendations

## Training Data

- Construction site safety videos
- Expert-annotated safety violations and recommendations
- Multiple analysis perspectives (comprehensive, prediction, remediation)

## Limitations

- Trained on limited construction scenarios
- May not cover all possible safety situations
- Requires high-quality video input for best performance
- Should be used as a tool to assist human safety inspectors, not replace them

## Model Architecture

- Multimodal transformer architecture
- Video processing: up to 128 frames at 4 FPS
- Audio processing: 16kHz sampling rate
- Text generation: Construction safety domain expertise

## License

Please refer to the original NVIDIA OmniVinci license for usage terms.
"""

        model_card_path = merged_model_path / "README.md"
        with open(model_card_path, 'w') as f:
            f.write(model_card_content.strip())

        logger.info(f"Model card created at {model_card_path}")

def main():
    """Main function for model merging."""

    print("OmniVinci Model Merger")
    print("=" * 40)

    merger = ModelMerger()

    # Check if LoRA adapter exists
    if not merger.finetuned_path.exists():
        print(f"Error: No fine-tuned model found at {merger.finetuned_path}")
        print("Please run the training pipeline first.")
        return

    try:
        # Merge LoRA weights
        print("Merging LoRA weights with base model...")
        merged_path = merger.merge_lora_weights()

        # Validate merged model
        print("Validating merged model...")
        if merger.validate_merged_model(merged_path):
            print("Model validation passed!")
        else:
            print("Warning: Model validation failed")

        # Create model card
        print("Creating model card...")
        merger.create_model_card(merged_path)

        print(f"\nModel merge complete!")
        print(f"Merged model saved to: {merged_path}")
        print("\nThe merged model can now be used independently without LoRA adapters.")

        # Print usage instructions
        print(f"\nUsage:")
        print(f"```python")
        print(f"from transformers import AutoProcessor, AutoModel")
        print(f"")
        print(f"model = AutoModel.from_pretrained('{merged_path}', trust_remote_code=True)")
        print(f"processor = AutoProcessor.from_pretrained('{merged_path}', trust_remote_code=True)")
        print(f"```")

    except Exception as e:
        print(f"Error during model merge: {e}")
        raise

if __name__ == "__main__":
    main()