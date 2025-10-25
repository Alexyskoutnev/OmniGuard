"""
Training pipeline for NVIDIA OmniVinci construction safety analysis
"""

import os
import json
import torch
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import logging
from datetime import datetime

from transformers import (
    AutoProcessor, AutoModel, AutoConfig,
    TrainingArguments, Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig, get_peft_model, TaskType,
    prepare_model_for_kbit_training
)
from datasets import Dataset
import accelerate

# Add parent directories to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import (
    OMNIVINCI_MODEL_PATH, TRAINING_CONFIG, LORA_CONFIG, OUTPUT_DIR
)
from src.data.dataset import OmniVinciDataset
from src.data.simple_hf_loader import load_construction_safety_dataset, ConstructionSafetyHFDataset
from src.data.annotation_templates import ScalableDatasetGenerator
from src.data.jsonl_dataset_loader import JSONLConstructionSafetyDataset
from src.utils.model_utils import ModelManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Training configuration for OmniVinci fine-tuning."""

    model_path: str = OMNIVINCI_MODEL_PATH
    dataset_path: str = str(OUTPUT_DIR / "training_dataset.json")
    jsonl_dataset_path: str = "src/data/datasets/dataset"  # Path to JSONL dataset
    output_dir: str = str(OUTPUT_DIR / "finetuned_model")
    use_jsonl_dataset: bool = True  # Use JSONL format by default

    # Training hyperparameters
    num_train_epochs: int = TRAINING_CONFIG["num_epochs"]
    per_device_train_batch_size: int = TRAINING_CONFIG["batch_size"]
    gradient_accumulation_steps: int = TRAINING_CONFIG["gradient_accumulation_steps"]
    learning_rate: float = TRAINING_CONFIG["learning_rate"]
    warmup_steps: int = TRAINING_CONFIG["warmup_steps"]
    max_grad_norm: float = TRAINING_CONFIG["max_grad_norm"]

    # Saving and evaluation
    save_steps: int = TRAINING_CONFIG["save_steps"]
    eval_steps: int = TRAINING_CONFIG["eval_steps"]
    save_total_limit: int = 3
    evaluation_strategy: str = "steps"
    save_strategy: str = "steps"

    # Memory optimization
    fp16: bool = True
    dataloader_pin_memory: bool = False
    remove_unused_columns: bool = False

    # Logging
    logging_steps: int = 50
    report_to: List[str] = field(default_factory=lambda: ["tensorboard"])

class OmniVinciTrainer:
    """Trainer for OmniVinci construction safety fine-tuning."""

    def __init__(self, config: TrainingConfig):
        self.config = config
        self.model_manager = ModelManager()
        self.model = None
        self.processor = None
        self.peft_model = None

    def setup_model(self):
        """Setup OmniVinci model and processor for training."""
        logger.info("Setting up model and processor for training")

        self.model, self.processor, _ = self.model_manager.load_model(
            self.config.model_path,
            for_training=True
        )

        # Configure model for training
        self.model.config.use_cache = False
        logger.info("Model setup complete")

    def setup_lora(self):
        """Setup LoRA configuration for efficient fine-tuning."""
        logger.info("Setting up LoRA configuration")

        # LoRA configuration
        lora_config = LoraConfig(
            r=LORA_CONFIG["r"],
            lora_alpha=LORA_CONFIG["lora_alpha"],
            target_modules=LORA_CONFIG["target_modules"],
            lora_dropout=LORA_CONFIG["lora_dropout"],
            bias=LORA_CONFIG["bias"],
            task_type=TaskType.CAUSAL_LM,
        )

        # Prepare model for training
        self.model = prepare_model_for_kbit_training(self.model)

        # Apply LoRA
        self.peft_model = get_peft_model(self.model, lora_config)

        # Print trainable parameters
        self.peft_model.print_trainable_parameters()
        logger.info("LoRA setup complete")

    def create_training_arguments(self) -> TrainingArguments:
        """Create training arguments for the trainer."""
        return TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            learning_rate=self.config.learning_rate,
            warmup_steps=self.config.warmup_steps,
            max_grad_norm=self.config.max_grad_norm,
            save_steps=self.config.save_steps,
            eval_steps=self.config.eval_steps,
            save_total_limit=self.config.save_total_limit,
            evaluation_strategy=self.config.evaluation_strategy,
            save_strategy=self.config.save_strategy,
            fp16=self.config.fp16,
            dataloader_pin_memory=self.config.dataloader_pin_memory,
            remove_unused_columns=self.config.remove_unused_columns,
            logging_steps=self.config.logging_steps,
            report_to=self.config.report_to,
            run_name=f"omnivinci_construction_safety_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

    def prepare_hf_datasets(self, dataset_name: str, split: str = "train"):
        """Prepare training datasets from HuggingFace Hub."""
        logger.info(f"Preparing HuggingFace datasets from {dataset_name}")

        # Initialize HuggingFace dataset loader
        hf_loader = ConstructionSafetyHFDataset(self.processor)

        # Load and prepare dataset
        full_dataset = hf_loader.load_construction_dataset(
            dataset_name=dataset_name,
            split=split,
            validate=True,
            convert_format=True
        )

        # Split dataset for training and validation
        train_size = int(0.8 * len(full_dataset))
        val_size = len(full_dataset) - train_size

        train_dataset = full_dataset.select(range(train_size))
        eval_dataset = full_dataset.select(range(train_size, train_size + val_size)) if val_size > 0 else None

        logger.info(f"Training dataset size: {len(train_dataset)}")
        if eval_dataset:
            logger.info(f"Evaluation dataset size: {len(eval_dataset)}")

        return train_dataset, eval_dataset

    def prepare_jsonl_datasets(self):
        """Prepare training and validation datasets from JSONL format."""
        logger.info("Preparing JSONL datasets")

        # Create JSONL dataset loader
        jsonl_loader = JSONLConstructionSafetyDataset(
            self.config.jsonl_dataset_path,
            self.processor
        )

        # Load training dataset
        train_dataset = jsonl_loader.create_hf_dataset("train")

        # Load test dataset as evaluation data
        try:
            eval_dataset = jsonl_loader.create_hf_dataset("test")
        except Exception as e:
            logger.warning(f"Could not load test dataset for evaluation: {e}")
            # Split training data for evaluation
            train_size = int(0.8 * len(train_dataset))
            eval_dataset = train_dataset.select(range(train_size, len(train_dataset)))
            train_dataset = train_dataset.select(range(train_size))

        logger.info(f"Training dataset size: {len(train_dataset)}")
        logger.info(f"Evaluation dataset size: {len(eval_dataset)}")

        # Print dataset statistics
        try:
            stats = jsonl_loader.get_dataset_stats()
            logger.info(f"Dataset statistics: {stats}")
        except Exception as e:
            logger.warning(f"Could not get dataset statistics: {e}")

        return train_dataset, eval_dataset

    def prepare_datasets(self):
        """Prepare training and validation datasets (legacy local format)."""
        logger.info("Preparing datasets")

        # Create dataset handler
        dataset_handler = OmniVinciDataset(
            self.config.dataset_path,
            self.processor
        )

        # Create dataset
        full_dataset = dataset_handler.create_dataset()

        # Split dataset for training and validation
        train_size = int(0.8 * len(full_dataset))
        val_size = len(full_dataset) - train_size

        train_dataset = full_dataset.select(range(train_size))
        eval_dataset = full_dataset.select(range(train_size, train_size + val_size)) if val_size > 0 else None

        logger.info(f"Training dataset size: {len(train_dataset)}")
        if eval_dataset:
            logger.info(f"Evaluation dataset size: {len(eval_dataset)}")

        return train_dataset, eval_dataset

    def create_data_collator(self):
        """Create data collator for OmniVinci training."""
        def data_collator(features):
            batch = {}
            if features and features[0].get("input_ids") is not None:
                batch["input_ids"] = torch.stack([torch.tensor(f["input_ids"]) for f in features])
            return batch

        return data_collator

    def train(self):
        """Execute the training process."""
        logger.info("Starting OmniVinci fine-tuning process")

        # Setup model and LoRA
        self.setup_model()
        self.setup_lora()

        # Prepare datasets
        if self.config.use_jsonl_dataset:
            train_dataset, eval_dataset = self.prepare_jsonl_datasets()
        else:
            train_dataset, eval_dataset = self.prepare_datasets()

        # Create training arguments
        training_args = self.create_training_arguments()

        # Create data collator
        data_collator = self.create_data_collator()

        # Create trainer
        trainer = Trainer(
            model=self.peft_model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
        )

        # Start training
        logger.info("Beginning training...")
        trainer.train()

        # Save the final model
        final_model_path = Path(self.config.output_dir) / "final_model"
        trainer.save_model(str(final_model_path))
        self.processor.save_pretrained(str(final_model_path))

        logger.info(f"Training complete! Model saved to: {final_model_path}")
        return trainer

def main():
    """Main training function."""
    print("OmniVinci Construction Safety Training Pipeline")
    print("=" * 60)

    # Check dependencies
    config = TrainingConfig()

    # Check if JSONL dataset exists
    jsonl_dataset_path = Path(config.jsonl_dataset_path)
    legacy_dataset_path = OUTPUT_DIR / "training_dataset.json"

    if config.use_jsonl_dataset:
        if not jsonl_dataset_path.exists():
            print(f"Error: JSONL dataset not found at {jsonl_dataset_path}")
            print("Available dataset formats:")
            if legacy_dataset_path.exists():
                print(f"  - Legacy JSON format: {legacy_dataset_path}")
                print("  - Set use_jsonl_dataset=False to use legacy format")
            return
        else:
            print(f"Using JSONL dataset from: {jsonl_dataset_path}")
    else:
        if not legacy_dataset_path.exists():
            print(f"Error: Legacy training dataset not found at {legacy_dataset_path}")
            print("Please run data preparation scripts first or switch to JSONL format.")
            return
        else:
            print(f"Using legacy dataset from: {legacy_dataset_path}")

    model_path = Path(OMNIVINCI_MODEL_PATH)
    if not model_path.exists():
        print(f"Error: OmniVinci model not found at {model_path}")
        print("Please ensure the model is downloaded and available.")
        return

    # Create output directory
    Path(config.output_dir).mkdir(parents=True, exist_ok=True)

    # Display configuration
    print(f"Model path: {config.model_path}")
    print(f"Dataset path: {config.dataset_path}")
    print(f"Output directory: {config.output_dir}")
    print(f"Training epochs: {config.num_train_epochs}")
    print(f"Batch size: {config.per_device_train_batch_size}")
    print(f"Learning rate: {config.learning_rate}")

    # Check GPU
    if torch.cuda.is_available():
        print(f"CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("Warning: CUDA not available, training will be slow on CPU")

    try:
        # Create and run trainer
        trainer = OmniVinciTrainer(config)
        trainer.train()

        print("\nTraining completed successfully!")
        print(f"Fine-tuned model available at: {config.output_dir}")

    except Exception as e:
        logger.error(f"Training failed: {e}")
        print(f"Error during training: {e}")
        raise

if __name__ == "__main__":
    main()