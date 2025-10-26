from ..src.tools import tool
from .notification_tools import mock_911_call, mock_safety_api_call


@tool(description="Detect EMS emergencies and dispatch emergency services if needed")
def detect_ems_hazard(description: str) -> str:
    """
    Analyze scene for medical emergencies with severity scoring and automatic 911 dispatch
    """
    # Define weighted keywords for better detection
    critical_keywords = {
        "chest pain": 10,
        "heart attack": 10,
        "unconscious": 10,
        "not breathing": 10,
        "severe bleeding": 9,
        "allergic reaction": 8,
        "heat stroke": 8,
        "diabetic emergency": 7,
        "seizure": 9,
        "pale": 5,
        "sweating heavily": 6,
        "confusion": 6,
        "laceration": 7,
        "arterial bleed": 10,
    }

    # Calculate severity score
    severity_score = 0
    detected_conditions = []

    desc_lower = description.lower()
    for keyword, weight in critical_keywords.items():
        if keyword in desc_lower:
            severity_score += weight
            detected_conditions.append(keyword)

    if severity_score == 0:
        return "No immediate medical emergency detected. Continue routine health monitoring."

    # Determine severity level
    if severity_score >= 15:
        severity = "CRITICAL"
    elif severity_score >= 8:
        severity = "HIGH"
    else:
        severity = "MODERATE"

    # Build response
    response_parts = [f"⚠️ MEDICAL EMERGENCY DETECTED - Severity: {severity}"]
    response_parts.append(f"Conditions identified: {', '.join(detected_conditions)}")

    if severity in ["CRITICAL", "HIGH"]:
        # Call 911
        call_response = mock_911_call(
            location="Construction Site - GPS coordinates logged",
            emergency_type="Medical Emergency",
            description=f"Worker showing signs of: {', '.join(detected_conditions)}",
        )
        response_parts.append(f"\n✅ 911 DISPATCHED - Call ID: {call_response['call_id']}")
        response_parts.append(f"ETA: {call_response['estimated_arrival']}")
        response_parts.append(f"Units: {', '.join(call_response['units_dispatched'])}")

        # Log to safety system
        api_response = mock_safety_api_call(
            incident_type="Medical Emergency",
            severity=severity,
            data={"conditions": detected_conditions, "score": severity_score},
        )
        response_parts.append(f"\n📋 Incident logged: {api_response['incident_id']}")

    # Add immediate actions
    response_parts.append("\n🚨 IMMEDIATE ACTIONS:")
    response_parts.append("1. Do not move the worker unless immediate danger present")
    response_parts.append("2. Assign first aid responder to stay with worker")
    response_parts.append("3. Clear area and prepare for EMS arrival")
    response_parts.append("4. Have worker's medical info/medications ready")

    return "\n".join(response_parts)
