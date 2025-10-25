"""
Evaluation pipeline for construction safety analysis model
"""

import json
import torch
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
import numpy as np
from datetime import datetime
import re

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import OUTPUT_DIR, DATASET_DIR
from src.train.inference import SafetyInferenceEngine, SafetyAnalysisResult
from src.data.safety_annotation_schema import ConstructionSafetyAnnotation, create_example_annotations

@dataclass
class EvaluationMetrics:
    """Evaluation metrics for safety analysis."""

    # Basic metrics
    total_predictions: int = 0
    correct_predictions: int = 0
    accuracy: float = 0.0

    # Safety-specific metrics
    safety_violation_detection_rate: float = 0.0
    false_positive_rate: float = 0.0
    risk_level_accuracy: float = 0.0

    # Content quality metrics
    average_confidence: float = 0.0
    average_response_length: int = 0
    structured_response_rate: float = 0.0

    # Performance metrics
    average_processing_time: float = 0.0

    # Detailed breakdowns
    risk_level_breakdown: Dict[str, Dict[str, int]] = field(default_factory=dict)
    incident_type_breakdown: Dict[str, Dict[str, int]] = field(default_factory=dict)

class SafetyAnalysisEvaluator:
    """Evaluator for construction safety analysis models."""

    def __init__(self, base_model_path: str = None):
        self.base_model_path = base_model_path
        self.ground_truth_annotations = self._load_ground_truth()

    def _load_ground_truth(self) -> List[ConstructionSafetyAnnotation]:
        """Load ground truth annotations for evaluation."""
        # For this implementation, we'll use the example annotations
        # In a real scenario, you'd load actual human-annotated ground truth
        return create_example_annotations()

    def evaluate_model(self, use_finetuned: bool = True) -> EvaluationMetrics:
        """Evaluate the model against ground truth annotations."""

        print("Starting Model Evaluation")
        print("=" * 50)
        print(f"Model type: {'Fine-tuned' if use_finetuned else 'Base'}")
        print(f"Ground truth samples: {len(self.ground_truth_annotations)}")

        # Initialize inference engine
        inference_engine = SafetyInferenceEngine(use_finetuned=use_finetuned)
        inference_engine.load_model()

        # Collect all predictions
        all_results = []
        for annotation in self.ground_truth_annotations:
            video_path = DATASET_DIR / annotation.video_filename

            if not video_path.exists():
                print(f"Warning: Video {annotation.video_filename} not found, skipping")
                continue

            print(f"Evaluating: {annotation.video_filename}")

            # Get comprehensive analysis
            result = inference_engine.analyze_video(
                video_path,
                analysis_type="comprehensive"
            )
            all_results.append((result, annotation))

        # Calculate metrics
        metrics = self._calculate_metrics(all_results)
        return metrics

    def _calculate_metrics(self, results: List[Tuple[SafetyAnalysisResult, ConstructionSafetyAnnotation]]) -> EvaluationMetrics:
        """Calculate evaluation metrics from results."""

        metrics = EvaluationMetrics()
        metrics.total_predictions = len(results)

        if not results:
            return metrics

        # Initialize counters
        correct_risk_levels = 0
        detected_violations = 0
        total_violations = 0
        structured_responses = 0
        total_response_length = 0
        total_confidence = 0.0
        total_processing_time = 0.0

        risk_level_breakdown = {}
        incident_type_breakdown = {}

        for result, ground_truth in results:
            prediction = result.prediction
            gt_risk_level = ground_truth.overall_safety_status.value

            # Extract predicted risk level from response
            predicted_risk_level = self._extract_risk_level(prediction)

            # Risk level accuracy
            if predicted_risk_level == gt_risk_level:
                correct_risk_levels += 1

            # Track risk level breakdown
            if gt_risk_level not in risk_level_breakdown:
                risk_level_breakdown[gt_risk_level] = {"correct": 0, "total": 0}
            risk_level_breakdown[gt_risk_level]["total"] += 1
            if predicted_risk_level == gt_risk_level:
                risk_level_breakdown[gt_risk_level]["correct"] += 1

            # Safety violation detection
            predicted_violations = self._extract_violations(prediction)
            gt_violations = [v.incident_type.value for v in ground_truth.violations]

            total_violations += len(gt_violations)
            for violation in gt_violations:
                if any(violation.replace("_", " ").lower() in pred.lower() for pred in predicted_violations):
                    detected_violations += 1

                # Track incident type breakdown
                if violation not in incident_type_breakdown:
                    incident_type_breakdown[violation] = {"detected": 0, "total": 0}
                incident_type_breakdown[violation]["total"] += 1
                if any(violation.replace("_", " ").lower() in pred.lower() for pred in predicted_violations):
                    incident_type_breakdown[violation]["detected"] += 1

            # Response quality metrics
            if self._is_structured_response(prediction):
                structured_responses += 1

            total_response_length += len(prediction)
            total_confidence += result.confidence_score
            total_processing_time += result.processing_time

        # Calculate final metrics
        metrics.accuracy = correct_risk_levels / metrics.total_predictions if metrics.total_predictions > 0 else 0
        metrics.risk_level_accuracy = correct_risk_levels / metrics.total_predictions if metrics.total_predictions > 0 else 0
        metrics.safety_violation_detection_rate = detected_violations / total_violations if total_violations > 0 else 0
        metrics.structured_response_rate = structured_responses / metrics.total_predictions if metrics.total_predictions > 0 else 0
        metrics.average_confidence = total_confidence / metrics.total_predictions if metrics.total_predictions > 0 else 0
        metrics.average_response_length = int(total_response_length / metrics.total_predictions) if metrics.total_predictions > 0 else 0
        metrics.average_processing_time = total_processing_time / metrics.total_predictions if metrics.total_predictions > 0 else 0
        metrics.risk_level_breakdown = risk_level_breakdown
        metrics.incident_type_breakdown = incident_type_breakdown

        return metrics

    def _extract_risk_level(self, prediction: str) -> str:
        """Extract predicted risk level from model response."""
        prediction_lower = prediction.lower()

        # Look for explicit risk level mentions
        risk_patterns = [
            r"safety status:\s*(\w+)",
            r"risk level:\s*(\w+)",
            r"overall.*risk:\s*(\w+)",
            r"risk:\s*(\w+)"
        ]

        for pattern in risk_patterns:
            match = re.search(pattern, prediction_lower)
            if match:
                risk_level = match.group(1)
                if risk_level in ["low", "medium", "high", "critical"]:
                    return risk_level

        # If no explicit mention, infer from content
        if "critical" in prediction_lower or "severe" in prediction_lower:
            return "critical"
        elif "high" in prediction_lower or "dangerous" in prediction_lower:
            return "high"
        elif "medium" in prediction_lower or "moderate" in prediction_lower:
            return "medium"
        else:
            return "low"

    def _extract_violations(self, prediction: str) -> List[str]:
        """Extract mentioned safety violations from prediction."""
        violations = []
        prediction_lower = prediction.lower()

        # Common violation keywords
        violation_keywords = {
            "ppe violation": ["ppe", "helmet", "hard hat", "safety vest", "gloves"],
            "fall hazard": ["fall", "height", "scaffolding", "ladder"],
            "equipment malfunction": ["equipment", "malfunction", "broken", "faulty"],
            "unsafe behavior": ["unsafe", "behavior", "careless", "reckless"],
            "environmental hazard": ["environmental", "weather", "conditions"],
        }

        for violation_type, keywords in violation_keywords.items():
            if any(keyword in prediction_lower for keyword in keywords):
                violations.append(violation_type)

        return violations

    def _is_structured_response(self, prediction: str) -> bool:
        """Check if response follows structured format."""
        structure_markers = [
            "SAFETY STATUS:",
            "VIOLATIONS:",
            "REMEDIATION:",
            "PREDICTIONS:",
            "WORKERS:",
            "DESCRIPTION:"
        ]

        return any(marker in prediction.upper() for marker in structure_markers)

    def compare_models(self) -> Dict[str, EvaluationMetrics]:
        """Compare base model vs fine-tuned model performance."""

        print("Comparing Base Model vs Fine-tuned Model")
        print("=" * 60)

        results = {}

        # Evaluate base model
        print("Evaluating base model...")
        try:
            base_metrics = self.evaluate_model(use_finetuned=False)
            results["base"] = base_metrics
            print("Base model evaluation complete")
        except Exception as e:
            print(f"Base model evaluation failed: {e}")
            results["base"] = None

        # Evaluate fine-tuned model
        print("\nEvaluating fine-tuned model...")
        try:
            finetuned_metrics = self.evaluate_model(use_finetuned=True)
            results["finetuned"] = finetuned_metrics
            print("Fine-tuned model evaluation complete")
        except Exception as e:
            print(f"Fine-tuned model evaluation failed: {e}")
            results["finetuned"] = None

        return results

    def generate_evaluation_report(self, metrics: EvaluationMetrics, model_type: str = "model") -> str:
        """Generate detailed evaluation report."""

        lines = []
        lines.append(f"EVALUATION REPORT: {model_type.upper()}")
        lines.append("=" * 50)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Overall metrics
        lines.append("OVERALL PERFORMANCE:")
        lines.append(f"  Total Predictions: {metrics.total_predictions}")
        lines.append(f"  Risk Level Accuracy: {metrics.risk_level_accuracy:.3f}")
        lines.append(f"  Violation Detection Rate: {metrics.safety_violation_detection_rate:.3f}")
        lines.append(f"  Average Confidence: {metrics.average_confidence:.3f}")
        lines.append(f"  Average Processing Time: {metrics.average_processing_time:.2f}s")
        lines.append("")

        # Response quality
        lines.append("RESPONSE QUALITY:")
        lines.append(f"  Structured Response Rate: {metrics.structured_response_rate:.3f}")
        lines.append(f"  Average Response Length: {metrics.average_response_length} characters")
        lines.append("")

        # Risk level breakdown
        if metrics.risk_level_breakdown:
            lines.append("RISK LEVEL BREAKDOWN:")
            for risk_level, data in metrics.risk_level_breakdown.items():
                accuracy = data["correct"] / data["total"] if data["total"] > 0 else 0
                lines.append(f"  {risk_level.capitalize()}: {accuracy:.3f} ({data['correct']}/{data['total']})")
            lines.append("")

        # Incident type breakdown
        if metrics.incident_type_breakdown:
            lines.append("INCIDENT TYPE DETECTION:")
            for incident_type, data in metrics.incident_type_breakdown.items():
                detection_rate = data["detected"] / data["total"] if data["total"] > 0 else 0
                lines.append(f"  {incident_type.replace('_', ' ').title()}: {detection_rate:.3f} ({data['detected']}/{data['total']})")
            lines.append("")

        return "\n".join(lines)

    def save_evaluation_results(self, results: Dict[str, EvaluationMetrics]):
        """Save evaluation results to files."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON results
        json_results = {}
        for model_type, metrics in results.items():
            if metrics:
                json_results[model_type] = {
                    "total_predictions": metrics.total_predictions,
                    "accuracy": metrics.accuracy,
                    "risk_level_accuracy": metrics.risk_level_accuracy,
                    "safety_violation_detection_rate": metrics.safety_violation_detection_rate,
                    "average_confidence": metrics.average_confidence,
                    "average_response_length": metrics.average_response_length,
                    "structured_response_rate": metrics.structured_response_rate,
                    "average_processing_time": metrics.average_processing_time,
                    "risk_level_breakdown": metrics.risk_level_breakdown,
                    "incident_type_breakdown": metrics.incident_type_breakdown
                }

        json_file = OUTPUT_DIR / f"evaluation_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(json_results, f, indent=2)

        # Save detailed reports
        for model_type, metrics in results.items():
            if metrics:
                report = self.generate_evaluation_report(metrics, model_type)
                report_file = OUTPUT_DIR / f"evaluation_report_{model_type}_{timestamp}.txt"
                with open(report_file, 'w') as f:
                    f.write(report)
                print(f"Evaluation report saved: {report_file}")

        print(f"Evaluation results saved: {json_file}")

def main():
    """Main evaluation function."""

    print("Construction Safety Model Evaluation")
    print("=" * 60)

    evaluator = SafetyAnalysisEvaluator()

    # Compare models
    results = evaluator.compare_models()

    # Save results
    evaluator.save_evaluation_results(results)

    # Print comparison summary
    print("\nEVALUATION SUMMARY:")
    print("-" * 30)

    for model_type, metrics in results.items():
        if metrics:
            print(f"\n{model_type.upper()} MODEL:")
            print(f"  Risk Level Accuracy: {metrics.risk_level_accuracy:.3f}")
            print(f"  Violation Detection: {metrics.safety_violation_detection_rate:.3f}")
            print(f"  Avg Confidence: {metrics.average_confidence:.3f}")
            print(f"  Avg Processing Time: {metrics.average_processing_time:.2f}s")
        else:
            print(f"\n{model_type.upper()} MODEL: Evaluation failed")

    # Show improvement if both models evaluated
    if results.get("base") and results.get("finetuned"):
        base_acc = results["base"].risk_level_accuracy
        ft_acc = results["finetuned"].risk_level_accuracy
        improvement = (ft_acc - base_acc) / base_acc * 100 if base_acc > 0 else 0
        print(f"\nFINE-TUNING IMPROVEMENT: {improvement:+.1f}%")

if __name__ == "__main__":
    main()