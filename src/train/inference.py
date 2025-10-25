"""
Inference pipeline for construction safety analysis using fine-tuned OmniVinci
"""

import torch
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import (
    OMNIVINCI_MODEL_PATH, DATASET_DIR, OUTPUT_DIR,
    VIDEO_CONFIG, AUDIO_CONFIG, SAFETY_PROMPTS, AGENT_CONFIG
)
from src.utils.model_utils import ModelManager

@dataclass
class SafetyAnalysisResult:
    """Result of safety analysis inference."""

    video_path: str
    analysis_type: str
    prediction: str
    confidence_score: float
    processing_time: float
    timestamp: str
    model_version: str

    def to_dict(self) -> Dict:
        return {
            "video_path": self.video_path,
            "analysis_type": self.analysis_type,
            "prediction": self.prediction,
            "confidence_score": self.confidence_score,
            "processing_time": self.processing_time,
            "timestamp": self.timestamp,
            "model_version": self.model_version
        }

    def to_agent_input(self, video_id: str = None) -> Dict:
        """Convert to simplified agent input format."""
        import json

        # Try to parse prediction as JSON
        try:
            pred_data = json.loads(self.prediction)
            safety_status = pred_data.get('safety_status', 'UNKNOWN').upper()
            scene_description = pred_data.get('description', 'No description available')

            # Extract predictions
            predictions = {
                "probability": self.confidence_score,
                "incident_type": "Unknown"
            }

            if 'predictions' in pred_data and pred_data['predictions']:
                first_prediction = pred_data['predictions'][0] if isinstance(pred_data['predictions'], list) else pred_data['predictions']
                predictions["incident_type"] = first_prediction.get('incident_type', 'Unknown')
                predictions["probability"] = first_prediction.get('probability', self.confidence_score)

            # Extract safety response
            safety_response = "No specific response provided"
            if 'safety_response' in pred_data:
                sr = pred_data['safety_response']
                if isinstance(sr, dict) and 'primary_action' in sr:
                    safety_response = sr['primary_action'].get('description', safety_response)
                elif isinstance(sr, str):
                    safety_response = sr

        except (json.JSONDecodeError, KeyError, TypeError):
            # Fallback to basic text analysis
            safety_status = "MEDIUM"
            scene_description = self.prediction[:200] + "..." if len(self.prediction) > 200 else self.prediction
            predictions = {"probability": self.confidence_score, "incident_type": "General safety concern"}
            safety_response = "Review situation and take appropriate safety measures"

        return {
            "video_id": video_id or Path(self.video_path).stem,
            "safety_status": safety_status,
            "scene_description": scene_description,
            "predictions": predictions,
            "safety_response": safety_response
        }

class SafetyInferenceEngine:
    """Inference engine for construction safety analysis."""

    def __init__(self, model_path: str = None, use_finetuned: bool = True, enable_agents: bool = None):
        self.base_model_path = model_path or OMNIVINCI_MODEL_PATH
        self.finetuned_model_path = OUTPUT_DIR / "finetuned_model" / "final_model"
        self.use_finetuned = use_finetuned and self.finetuned_model_path.exists()

        # Agent system integration
        self.enable_agents = enable_agents if enable_agents is not None else AGENT_CONFIG.get("enable_agents", False)
        self.safety_orchestrator = None

        if self.enable_agents:
            try:
                from src.agents.safety_agent import safety_orchestrator
                self.safety_orchestrator = safety_orchestrator
                print("Agent system integration enabled")
            except ImportError as e:
                print(f"Warning: Could not import agent system: {e}")
                self.enable_agents = False

        self.model_manager = ModelManager()
        self.model = None
        self.processor = None
        self.generation_config = None

        print(f"Initializing Safety Analysis Inference Engine")
        print(f"Base model: {self.base_model_path}")
        print(f"Agent execution: {'enabled' if self.enable_agents else 'disabled'}")
        if self.use_finetuned:
            print(f"Fine-tuned model: {self.finetuned_model_path}")
        else:
            print("Using base model (fine-tuned model not available)")

    def load_model(self):
        """Load the model and processor for inference."""
        print("Loading model and processor...")

        try:
            if self.use_finetuned:
                self.model, self.processor, _ = self.model_manager.load_finetuned_model(
                    str(self.base_model_path),
                    str(self.finetuned_model_path)
                )
                print("Fine-tuned model loaded successfully")
            else:
                self.model, self.processor, _ = self.model_manager.load_model(
                    self.base_model_path,
                    for_training=False
                )
                print("Base model loaded successfully")

            # Setup generation config
            self.generation_config = self.model.default_generation_config
            self.generation_config.update({
                "max_new_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            })

            print("Model loading complete")

        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def analyze_video(
        self,
        video_path: Union[str, Path],
        analysis_type: str = "comprehensive",
        custom_prompt: str = None
    ) -> SafetyAnalysisResult:
        """Analyze a single video for safety concerns."""

        if not self.model or not self.processor:
            self.load_model()

        video_path = str(video_path)
        start_time = time.time()

        # Select appropriate prompt
        if custom_prompt:
            prompt = custom_prompt
        elif analysis_type == "comprehensive":
            prompt = SAFETY_PROMPTS["analysis"]
        elif analysis_type == "prediction":
            prompt = SAFETY_PROMPTS["prediction"]
        elif analysis_type == "remediation":
            prompt = SAFETY_PROMPTS["remediation"]
        else:
            prompt = "Analyze this construction site video for safety concerns."

        try:
            print(f"Analyzing video: {Path(video_path).name}")
            print(f"Analysis type: {analysis_type}")

            # Create conversation format
            conversation = [{
                "role": "user",
                "content": [
                    {"type": "video", "video": video_path},
                    {"type": "text", "text": prompt}
                ]
            }]

            # Apply chat template
            text = self.processor.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )

            # Process inputs
            inputs = self.processor([text])

            # Generate response
            print("Generating safety analysis...")
            with torch.no_grad():
                output_ids = self.model.generate(
                    input_ids=inputs.input_ids,
                    media=getattr(inputs, 'media', None),
                    media_config=getattr(inputs, 'media_config', None),
                    generation_config=self.generation_config,
                )

            # Decode response
            response = self.processor.tokenizer.batch_decode(
                output_ids,
                skip_special_tokens=True
            )[0]

            # Extract assistant's response
            if "assistant" in response.lower():
                assistant_start = response.lower().find("assistant")
                response = response[assistant_start:].split("\n", 1)[-1].strip()

            processing_time = time.time() - start_time
            confidence_score = self._calculate_confidence(response)

            result = SafetyAnalysisResult(
                video_path=video_path,
                analysis_type=analysis_type,
                prediction=response,
                confidence_score=confidence_score,
                processing_time=processing_time,
                timestamp=datetime.now().isoformat(),
                model_version="finetuned" if self.use_finetuned else "base"
            )

            print(f"Analysis complete in {processing_time:.2f} seconds")
            return result

        except Exception as e:
            print(f"Error during inference: {e}")
            raise

    def _calculate_confidence(self, response: str) -> float:
        """Calculate a confidence score for the response."""
        score = 0.5  # Base score

        # Check for key safety terms
        safety_keywords = [
            "hazard", "risk", "violation", "safety", "ppe", "helmet",
            "fall", "equipment", "remediation", "immediate", "critical"
        ]

        keyword_count = sum(1 for keyword in safety_keywords if keyword.lower() in response.lower())
        score += min(keyword_count * 0.05, 0.3)

        # Check response length
        if 50 < len(response) < 1000:
            score += 0.1
        elif len(response) >= 1000:
            score += 0.2

        # Check for structured response
        if any(marker in response for marker in ["SAFETY STATUS:", "VIOLATIONS:", "REMEDIATION:"]):
            score += 0.1

        return min(score, 1.0)

    def batch_analyze(self, video_directory: Path = None) -> List[SafetyAnalysisResult]:
        """Analyze multiple videos in batch."""
        if video_directory is None:
            video_directory = DATASET_DIR

        video_files = list(video_directory.glob("*.mp4"))

        if not video_files:
            print(f"No video files found in {video_directory}")
            return []

        print(f"Found {len(video_files)} videos to analyze")

        results = []
        for video_file in video_files:
            print(f"\nProcessing {video_file.name}...")

            # Perform different types of analysis
            for analysis_type in ["comprehensive", "prediction", "remediation"]:
                result = self.analyze_video(video_file, analysis_type)
                results.append(result)

        return results

    def save_results(self, results: List[SafetyAnalysisResult], output_file: Path = None):
        """Save analysis results to file."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = OUTPUT_DIR / f"safety_analysis_results_{timestamp}.json"

        results_data = {
            "analysis_metadata": {
                "total_analyses": len(results),
                "model_version": "finetuned" if self.use_finetuned else "base",
                "generation_timestamp": datetime.now().isoformat(),
                "average_processing_time": sum(r.processing_time for r in results) / len(results) if results else 0
            },
            "results": [result.to_dict() for result in results]
        }

        with open(output_file, 'w') as f:
            json.dump(results_data, f, indent=2)

        print(f"Results saved to: {output_file}")

    def generate_safety_report(self, results: List[SafetyAnalysisResult]) -> str:
        """Generate a summary safety report from analysis results."""
        if not results:
            return "No analysis results available."

        report_lines = []
        report_lines.append("CONSTRUCTION SITE SAFETY ANALYSIS REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Model: {'Fine-tuned OmniVinci' if self.use_finetuned else 'Base OmniVinci'}")
        report_lines.append("")

        # Group results by video
        videos = {}
        for result in results:
            video_name = Path(result.video_path).name
            if video_name not in videos:
                videos[video_name] = []
            videos[video_name].append(result)

        # Generate report for each video
        for video_name, video_results in videos.items():
            report_lines.append(f"VIDEO: {video_name}")
            report_lines.append("-" * 30)

            for result in video_results:
                report_lines.append(f"\n{result.analysis_type.upper()} ANALYSIS:")
                report_lines.append(f"Confidence: {result.confidence_score:.2f}")
                report_lines.append(f"Processing time: {result.processing_time:.2f}s")
                report_lines.append("")
                report_lines.append(result.prediction)
                report_lines.append("")

            report_lines.append("=" * 50)
            report_lines.append("")

        return "\n".join(report_lines)

def main():
    """Main inference function."""
    print("Construction Safety Analysis Inference Pipeline")
    print("=" * 60)

    # Initialize inference engine
    inference = SafetyInferenceEngine()

    try:
        # Load model
        inference.load_model()

        # Analyze all videos in dataset
        results = inference.batch_analyze()

        if results:
            # Save results
            inference.save_results(results)

            # Generate and save report
            report = inference.generate_safety_report(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = OUTPUT_DIR / f"safety_report_{timestamp}.txt"

            with open(report_file, 'w') as f:
                f.write(report)

            print(f"\nSafety report saved to: {report_file}")

            # Print summary
            print(f"\nAnalysis Summary:")
            print(f"- Total analyses: {len(results)}")
            print(f"- Average confidence: {sum(r.confidence_score for r in results) / len(results):.2f}")
            print(f"- Average processing time: {sum(r.processing_time for r in results) / len(results):.2f}s")

        else:
            print("No videos found to analyze")

    except Exception as e:
        print(f"Error during inference: {e}")
        raise

if __name__ == "__main__":
    main()