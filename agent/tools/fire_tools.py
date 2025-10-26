"""
Fire safety detection tools
"""

from ..src.tools import tool
from .notification_tools import mock_911_call, mock_safety_api_call


@tool(description="Detect fire hazards and alert fire services if needed")
def detect_fire_hazard(description: str) -> str:
    """
    Analyze scene for fire hazards with risk scoring and automatic fire department notification
    """
    risk_keywords = {
        "fire": 10,
        "flames": 10,
        "smoke visible": 9,
        "sparks": 6,
        "combustible": 7,
        "welding": 5,
        "fuel": 8,
        "oily rags": 7,
        "electrical overload": 8,
        "battery thermal": 9,
        "ignition": 8,
        "gas leak": 10,
        "explosion": 10,
        "smoldering": 8,
    }

    risk_score = 0
    detected_hazards = []

    desc_lower = description.lower()
    for keyword, weight in risk_keywords.items():
        if keyword in desc_lower:
            risk_score += weight
            detected_hazards.append(keyword)

    if risk_score == 0:
        return "No active fire hazards detected. Maintain fire prevention protocols."

    # Determine risk level
    if risk_score >= 15:
        risk_level = "CRITICAL"
    elif risk_score >= 8:
        risk_level = "HIGH"
    else:
        risk_level = "MODERATE"

    response_parts = [f"🔥 FIRE HAZARD DETECTED - Risk Level: {risk_level}"]
    response_parts.append(f"Hazards identified: {', '.join(detected_hazards)}")

    if risk_level in ["CRITICAL", "HIGH"]:
        # Call 911 for fire
        call_response = mock_911_call(
            location="Construction Site - Building/zone coordinates logged",
            emergency_type="Fire Emergency",
            description=f"Fire hazard: {', '.join(detected_hazards)}",
        )
        response_parts.append(
            f"\n✅ FIRE DEPARTMENT DISPATCHED - Call ID: {call_response['call_id']}"
        )
        response_parts.append(f"ETA: {call_response['estimated_arrival']}")

        # Log to safety system
        api_response = mock_safety_api_call(
            incident_type="Fire Hazard",
            severity=risk_level,
            data={"hazards": detected_hazards, "risk_score": risk_score},
        )
        response_parts.append(f"\n📋 Fire incident logged: {api_response['incident_id']}")

    response_parts.append("\n🚨 IMMEDIATE ACTIONS:")
    response_parts.append("1. EVACUATE immediate area")
    response_parts.append("2. Use fire extinguisher only if safe and trained")
    response_parts.append("3. Activate fire alarm system")
    response_parts.append("4. Account for all personnel at muster point")
    response_parts.append("5. Shut off utilities if safe to do so")

    return "\n".join(response_parts)
