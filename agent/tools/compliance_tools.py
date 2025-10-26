"""
PPE compliance and safety violation detection tools
"""

from ..src.tools import tool
from .notification_tools import mock_safety_api_call


@tool(description="Detect PPE violations and enforce compliance")
def detect_compliance_violation(description: str) -> str:
    violation_keywords = {
        "no hard hat": 9,
        "missing hard hat": 9,
        "without hard hat": 9,
        "no harness": 10,
        "no fall protection": 10,
        "no safety glasses": 7,
        "no hearing protection": 6,
        "no high-vis": 8,
        "no vest": 8,
        "no respirator": 8,
        "improper ppe": 6,
    }

    violation_score = 0
    detected_violations = []

    desc_lower = description.lower()
    for keyword, weight in violation_keywords.items():
        if keyword in desc_lower:
            violation_score += weight
            detected_violations.append(keyword)

    if violation_score == 0:
        return "PPE compliance satisfactory. Continue monitoring."

    if violation_score >= 9:
        severity = "CRITICAL"
    elif violation_score >= 6:
        severity = "HIGH"
    else:
        severity = "MODERATE"

    response_parts = [f"🦺 PPE VIOLATION DETECTED - Severity: {severity}"]
    response_parts.append(f"Violations: {', '.join(detected_violations)}")

    # Log to safety system
    api_response = mock_safety_api_call(
        incident_type="PPE Compliance Violation",
        severity=severity,
        data={"violations": detected_violations, "violation_score": violation_score},
    )
    response_parts.append(f"\n📋 Violation logged: {api_response['incident_id']}")

    if severity == "CRITICAL":
        response_parts.append("\n🛑 WORK STOPPAGE ISSUED")
        response_parts.append("Site supervisor and safety manager notified")

    response_parts.append("\n✅ COMPLIANCE ACTIONS:")
    response_parts.append("1. Stop worker - no entry to hazard area")
    response_parts.append("2. Provide required PPE immediately")
    response_parts.append("3. Document violation in worker file")
    response_parts.append("4. Retrain on PPE requirements")
    response_parts.append("5. Verify PPE fit and proper use before resuming work")

    return "\n".join(response_parts)
