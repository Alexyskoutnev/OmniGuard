"""
Model management utilities for OmniVinci
"""

import torch
from pathlib import Path
from typing import Tuple, Optional, Any
from transformers import AutoProcessor, AutoModel, AutoConfig
from peft import PeftModel

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import VIDEO_CONFIG, AUDIO_CONFIG

class ModelManager:
    """Centralized model management for OmniVinci."""

    def __init__(self):
        self.models = {}
        self.processors = {}

    def load_model(
        self,
        model_path: str,
        for_training: bool = False,
        cache_key: str = None
    ) -> Tuple[Any, Any, Any]:
        """
        Load OmniVinci model and processor.

        Args:
            model_path: Path to the model directory
            for_training: Whether to configure for training
            cache_key: Optional cache key for model reuse

        Returns:
            Tuple of (model, processor, config)
        """

        if cache_key and cache_key in self.models:
            return self.models[cache_key], self.processors[cache_key], None

        print(f"Loading model from: {model_path}")

        # Load configuration
        config = AutoConfig.from_pretrained(
            model_path,
            trust_remote_code=True
        )

        # Load model with appropriate settings
        model = AutoModel.from_pretrained(
            model_path,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=not for_training  # Disable cache for training
        )

        # Load processor
        processor = AutoProcessor.from_pretrained(
            model_path,
            trust_remote_code=True
        )

        # Configure video and audio settings
        self._configure_multimodal_settings(model, processor)

        # Cache if requested
        if cache_key:
            self.models[cache_key] = model
            self.processors[cache_key] = processor

        return model, processor, config

    def load_finetuned_model(
        self,
        base_model_path: str,
        adapter_path: str,
        cache_key: str = None
    ) -> Tuple[Any, Any, Any]:
        """
        Load fine-tuned model with LoRA adapter.

        Args:
            base_model_path: Path to base model
            adapter_path: Path to LoRA adapter
            cache_key: Optional cache key

        Returns:
            Tuple of (model, processor, config)
        """

        if cache_key and cache_key in self.models:
            return self.models[cache_key], self.processors[cache_key], None

        print(f"Loading fine-tuned model:")
        print(f"  Base: {base_model_path}")
        print(f"  Adapter: {adapter_path}")

        # Load base model
        base_model, _, config = self.load_model(base_model_path, for_training=False)

        # Load LoRA adapter
        model = PeftModel.from_pretrained(
            base_model,
            adapter_path,
            torch_dtype=torch.float16
        )

        # Load processor (try adapter path first, fall back to base)
        try:
            processor = AutoProcessor.from_pretrained(
                adapter_path,
                trust_remote_code=True
            )
        except:
            processor = AutoProcessor.from_pretrained(
                base_model_path,
                trust_remote_code=True
            )

        # Configure settings
        self._configure_multimodal_settings(model, processor)

        # Cache if requested
        if cache_key:
            self.models[cache_key] = model
            self.processors[cache_key] = processor

        return model, processor, config

    def _configure_multimodal_settings(self, model, processor):
        """Configure video and audio processing settings."""

        # Configure video settings
        model.config.num_video_frames = VIDEO_CONFIG["max_frames"]
        processor.config.num_video_frames = VIDEO_CONFIG["max_frames"]

        # Configure audio settings
        model.config.load_audio_in_video = AUDIO_CONFIG["load_audio"]
        processor.config.load_audio_in_video = AUDIO_CONFIG["load_audio"]

        if hasattr(model.config, 'audio_chunk_length'):
            model.config.audio_chunk_length = f"max_{AUDIO_CONFIG['max_duration']}"
            processor.config.audio_chunk_length = f"max_{AUDIO_CONFIG['max_duration']}"

    def clear_cache(self):
        """Clear cached models to free memory."""
        self.models.clear()
        self.processors.clear()
        torch.cuda.empty_cache()

    def get_model_info(self, model) -> dict:
        """Get information about a loaded model."""
        info = {
            "device": str(model.device) if hasattr(model, 'device') else "unknown",
            "dtype": str(model.dtype) if hasattr(model, 'dtype') else "unknown",
            "parameters": sum(p.numel() for p in model.parameters()),
            "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
        }

        # Add multimodal config info
        if hasattr(model, 'config'):
            config = model.config
            info["video_frames"] = getattr(config, 'num_video_frames', 'unknown')
            info["audio_enabled"] = getattr(config, 'load_audio_in_video', 'unknown')

        return info