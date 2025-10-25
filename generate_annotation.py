"""
Generate annotation using our safety annotation schema for the video
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.data.safety_annotation_schema import (
    ConstructionSafetyAnnotation, SafetyViolation, AccidentPrediction,
    SafetyResponse, PrimaryAction, EmergencyProtocol,
    IncidentType, RiskLevel, PPEType, PPEStatus,
    PrimaryActionType, EmergencyProtocolType
)
from datetime import datetime
import json

def generate_ladder_safety_annotation():
    """Generate annotation for the ladder safety video using our schema."""

    # Video information
    video_filename = "20251024_231728_4d32b541_video_68fc4dc296dc81919cf608d921c022c10c1147a9f503ce53.mp4"

    # Create the annotation
    annotation = ConstructionSafetyAnnotation(
        video_filename=video_filename,
        annotator_id="safety_expert_ai",
        annotation_timestamp=datetime.now().isoformat(),
        overall_safety_status=RiskLevel.CRITICAL,  # Highest risk level due to critical fall hazard
        general_description="Multi-story building construction with workers handling ladders. Multiple critical safety violations observed including unsecured ladders and unguarded openings.",
        worker_count=2,
        workers_with_proper_ppe=0,  # No visible PPE compliance mentioned
        equipment_present=["extension_ladders", "scaffolding", "construction_materials"],
        environmental_conditions="exterior_construction_site",
        site_type="commercial_construction",
        work_activity="ladder_setup_and_access",
        weather_conditions="clear"
    )

    # Add safety violations based on the existing annotation

    # 1. Unsafe worker behavior with ladder
    violation1 = SafetyViolation(
        incident_type=IncidentType.UNSAFE_BEHAVIOR,
        description="Worker setting up long extension ladder alone without assistance",
        risk_level=RiskLevel.MEDIUM,
        location_description="Ground level near building",
        timestamp_seconds=10.0,
        worker_count_affected=1,
        ppe_issues=[]  # No specific PPE issues mentioned for this violation
    )

    # 2. Fall hazard from unsecured ladders
    violation2 = SafetyViolation(
        incident_type=IncidentType.FALL_HAZARD,
        description="Extension ladders not secured at top or bottom, risk of displacement",
        risk_level=RiskLevel.HIGH,
        location_description="Ladders against building extending to second floor",
        timestamp_seconds=15.0,
        worker_count_affected=2,
        ppe_issues=[]
    )

    # 3. Unguarded floor openings - CRITICAL
    violation3 = SafetyViolation(
        incident_type=IncidentType.FALL_HAZARD,
        description="Second floor has open framing and large openings without guardrails or fall protection",
        risk_level=RiskLevel.CRITICAL,
        location_description="Second floor work area",
        timestamp_seconds=20.0,
        worker_count_affected=2,
        ppe_issues=[]
    )

    # 4. Unstable ladder base
    violation4 = SafetyViolation(
        incident_type=IncidentType.UNSAFE_BEHAVIOR,
        description="Ladder base placed on uneven ground (gravel/dirt) instead of firm surface",
        risk_level=RiskLevel.HIGH,
        location_description="Base of ladders on ground level",
        timestamp_seconds=5.0,
        worker_count_affected=2,
        ppe_issues=[]
    )

    # Add violations to annotation
    annotation.violations = [violation1, violation2, violation3, violation4]

    # Add accident predictions
    fall_prediction = AccidentPrediction(
        predicted_incident=IncidentType.FALL_HAZARD,
        probability=0.85,  # High probability due to multiple fall risks
        time_to_incident="immediate",
        contributing_factors=[
            "unsecured_ladders",
            "unguarded_openings",
            "unstable_ladder_base",
            "no_fall_protection",
            "single_worker_ladder_setup"
        ],
        severity_if_occurs=RiskLevel.CRITICAL
    )

    annotation.accident_predictions = [fall_prediction]

    # Create safety response with primary action and emergency protocols
    primary_action = PrimaryAction(
        action_type=PrimaryActionType.STOP_WORK_IMMEDIATELY,
        description="Stop all work at height immediately and secure ladders before resuming",
        timeline="immediate",
        responsible_party="site_supervisor"
    )

    # Emergency protocols
    emergency_protocols = [
        EmergencyProtocol(
            protocol_type=EmergencyProtocolType.CALL_911,
            trigger_condition="if_fall_injury_occurs",
            contact_info="911"
        ),
        EmergencyProtocol(
            protocol_type=EmergencyProtocolType.SITE_EVACUATION,
            trigger_condition="if_structural_instability_detected",
            contact_info="site_emergency_contacts"
        ),
        EmergencyProtocol(
            protocol_type=EmergencyProtocolType.NOTIFY_OSHA,
            trigger_condition="serious_injury_or_near_miss",
            contact_info="osha_reporting_line"
        )
    ]

    safety_response = SafetyResponse(
        primary_action=primary_action,
        emergency_protocols=emergency_protocols,
        follow_up_required=True,
        follow_up_timeline="within_1_hour"
    )

    annotation.safety_response = safety_response

    return annotation

def generate_json_output(annotation):
    """Generate JSON output in our optimized format."""

    response_data = {
        "safety_status": annotation.overall_safety_status.value,
        "description": annotation.general_description,
        "violations": [],
        "workers": {
            "total_count": annotation.worker_count,
            "ppe_compliant": annotation.workers_with_proper_ppe,
            "ppe_compliance_rate": annotation.workers_with_proper_ppe / annotation.worker_count if annotation.worker_count > 0 else 0
        },
        "predictions": [],
        "safety_response": None
    }

    # Format violations
    for violation in annotation.violations:
        response_data["violations"].append({
            "type": violation.incident_type.value,
            "risk_level": violation.risk_level.value,
            "description": violation.description,
            "location": violation.location_description,
            "workers_affected": violation.worker_count_affected
        })

    # Format predictions
    for pred in annotation.accident_predictions:
        response_data["predictions"].append({
            "incident_type": pred.predicted_incident.value,
            "probability": pred.probability,
            "timeline": pred.time_to_incident,
            "contributing_factors": pred.contributing_factors,
            "severity": pred.severity_if_occurs.value
        })

    # Format safety response
    if annotation.safety_response:
        response_data["safety_response"] = {
            "primary_action": {
                "action": annotation.safety_response.primary_action.action_type.value,
                "description": annotation.safety_response.primary_action.description,
                "timeline": annotation.safety_response.primary_action.timeline,
                "responsible_party": annotation.safety_response.primary_action.responsible_party
            },
            "emergency_protocols": [
                {
                    "protocol": protocol.protocol_type.value,
                    "trigger": protocol.trigger_condition,
                    "contact": protocol.contact_info
                }
                for protocol in annotation.safety_response.emergency_protocols
            ],
            "follow_up_required": annotation.safety_response.follow_up_required,
            "follow_up_timeline": annotation.safety_response.follow_up_timeline
        }

    return response_data

def main():
    print("Generating Safety Annotation using Our Schema")
    print("=" * 60)

    # Generate annotation
    annotation = generate_ladder_safety_annotation()

    # Show structured annotation
    print("STRUCTURED ANNOTATION:")
    print(f"Video: {annotation.video_filename}")
    print(f"Overall Safety Status: {annotation.overall_safety_status.value.upper()}")
    print(f"Description: {annotation.general_description}")
    print(f"Workers: {annotation.worker_count} total, {annotation.workers_with_proper_ppe} PPE compliant")

    print(f"\nVIOLATIONS FOUND ({len(annotation.violations)}):")
    for i, violation in enumerate(annotation.violations, 1):
        print(f"{i}. {violation.incident_type.value.replace('_', ' ').title()}")
        print(f"   Risk: {violation.risk_level.value}")
        print(f"   Description: {violation.description}")
        print(f"   Location: {violation.location_description}")
        print()

    print(f"ACCIDENT PREDICTIONS ({len(annotation.accident_predictions)}):")
    for i, prediction in enumerate(annotation.accident_predictions, 1):
        print(f"{i}. {prediction.predicted_incident.value.replace('_', ' ').title()}")
        print(f"   Probability: {prediction.probability:.0%}")
        print(f"   Timeline: {prediction.time_to_incident}")
        print(f"   Severity if occurs: {prediction.severity_if_occurs.value}")
        print()

    print("SAFETY RESPONSE:")
    if annotation.safety_response:
        print(f"Primary Action: {annotation.safety_response.primary_action.description}")
        print(f"Timeline: {annotation.safety_response.primary_action.timeline}")
        print(f"Emergency Protocols: {len(annotation.safety_response.emergency_protocols)} configured")

    print("\n" + "=" * 60)
    print("JSON OUTPUT FORMAT (for training):")
    print("=" * 60)

    # Generate JSON output
    json_output = generate_json_output(annotation)
    print(json.dumps(json_output, indent=2))

    print("\n" + "=" * 60)
    print("TRAINING PROMPT FORMAT:")
    print("=" * 60)

    # Generate training prompt (simplified version)
    print("SAFETY STATUS: CRITICAL")
    print(f"DESCRIPTION: {annotation.general_description}")
    print(f"WORKERS: {annotation.worker_count} workers present, {(annotation.workers_with_proper_ppe/annotation.worker_count)*100:.0f}% PPE compliance")
    print("VIOLATIONS IDENTIFIED:")
    for i, violation in enumerate(annotation.violations, 1):
        print(f"{i}. {violation.incident_type.value.replace('_', ' ').title()}: {violation.description} (Risk: {violation.risk_level.value})")
    print("ACCIDENT PREDICTIONS:")
    for i, prediction in enumerate(annotation.accident_predictions, 1):
        print(f"{i}. {prediction.predicted_incident.value.replace('_', ' ').title()} - {prediction.probability:.0%} probability, {prediction.time_to_incident}")
    print("SAFETY RESPONSE:")
    if annotation.safety_response:
        print(f"Primary Action: {annotation.safety_response.primary_action.description}")
        print(f"Emergency Protocols: {len(annotation.safety_response.emergency_protocols)} protocols configured")

if __name__ == "__main__":
    main()