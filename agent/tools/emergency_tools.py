from datetime import datetime
from typing import Any

from ..src.tools import tool


def mock_911_call(location: str, emergency_type: str, description: str) -> dict[str, Any]:
    """Mock call to 911 emergency services"""
    call_id = f"911-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    response = {
        "call_id": call_id,
        "status": "dispatched",
        "estimated_arrival": "8-12 minutes",
        "units_dispatched": ["Ambulance 42", "Fire Engine 7"]
        if "fire" in emergency_type.lower()
        else ["Ambulance 42"],
        "dispatcher_notes": f"Emergency at {location}. {description}",
        "timestamp": datetime.now().isoformat(),
    }

    print("\n🚨 [MOCK 911 CALL]")
    print(f"   Call ID: {call_id}")
    print(f"   Location: {location}")
    print(f"   Type: {emergency_type}")
    print(f"   Status: {response['status'].upper()}")
    print(f"   ETA: {response['estimated_arrival']}")
    print(f"   Units: {', '.join(response['units_dispatched'])}")

    return response


def mock_safety_api_call(incident_type: str, severity: str, data: dict[str, Any]) -> dict[str, Any]:
    incident_id = f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    response = {
        "incident_id": incident_id,
        "status": "logged",
        "severity": severity,
        "notifications_sent": [
            "Safety Manager",
            "Site Supervisor",
            "OSHA Compliance Officer" if severity == "CRITICAL" else None,
        ],
        "actions_triggered": [
            "Work stoppage order issued" if severity == "CRITICAL" else "Safety alert issued",
            "Incident report generated",
            "Photo documentation requested",
        ],
        "timestamp": datetime.now().isoformat(),
    }

    print("\n📡 [MOCK SAFETY API]")
    print(f"   Incident ID: {incident_id}")
    print(f"   Type: {incident_type}")
    print(f"   Severity: {severity}")
    print(f"   Notifications: {len([n for n in response['notifications_sent'] if n])}")
    print(f"   Status: {response['status'].upper()}")

    return response


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

    # Mock 911 call for critical cases
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


@tool(description="Detect injury hazards and log safety incidents")
def detect_injury_hazard(description: str) -> str:
    """
    Analyze scene for injury risks with severity assessment and incident logging
    """
    hazard_keywords = {
        "caught in machinery": 10,
        "crushing": 9,
        "amputation": 10,
        "eye injury": 8,
        "flying debris": 7,
        "laceration": 6,
        "back strain": 5,
        "lifting": 4,
        "unguarded": 8,
        "sprain": 4,
        "slip": 5,
        "trip": 5,
        "fall": 7,
    }

    hazard_score = 0
    detected_hazards = []

    desc_lower = description.lower()
    for keyword, weight in hazard_keywords.items():
        if keyword in desc_lower:
            hazard_score += weight
            detected_hazards.append(keyword)

    if hazard_score == 0:
        return "No immediate injury hazards detected. Continue safe work practices."

    if hazard_score >= 12:
        severity = "HIGH"
    elif hazard_score >= 6:
        severity = "MODERATE"
    else:
        severity = "LOW"

    response_parts = [f"⚠️ INJURY HAZARD DETECTED - Severity: {severity}"]
    response_parts.append(f"Hazards identified: {', '.join(detected_hazards)}")

    # Log to safety system for all severities
    api_response = mock_safety_api_call(
        incident_type="Injury Hazard",
        severity=severity,
        data={"hazards": detected_hazards, "hazard_score": hazard_score},
    )
    response_parts.append(f"\n📋 Safety incident logged: {api_response['incident_id']}")
    response_parts.append(
        f"Notifications sent to: {', '.join([n for n in api_response['notifications_sent'] if n])}"
    )

    response_parts.append("\n🛡️ REQUIRED ACTIONS:")
    if severity == "HIGH":
        response_parts.append("1. STOP WORK IMMEDIATELY")
        response_parts.append("2. Isolate hazard area with barriers")
        response_parts.append("3. Safety stand-down meeting required")
    else:
        response_parts.append("1. Correct hazard before continuing work")
        response_parts.append("2. Review safe work procedures with crew")
    response_parts.append("3. Ensure all machine guards in place")
    response_parts.append("4. Verify proper PPE usage")
    response_parts.append("5. Document corrective actions taken")

    return "\n".join(response_parts)


@tool(description="Detect PPE violations and enforce compliance")
def detect_compliance_violation(description: str) -> str:
    """
    Analyze scene for PPE violations with automatic work stoppage for critical cases
    """
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


@tool(description="Detect heat illness risks and initiate cooling protocols")
def detect_heat_hazard(description: str) -> str:
    """
    Analyze scene for heat illness with symptom severity and cooling intervention
    """
    heat_keywords = {
        "heat stroke": 10,
        "confused": 8,
        "unconscious": 10,
        "not sweating": 9,
        "dry skin": 9,
        "dizzy": 7,
        "nausea": 6,
        "temperature": 5,
        "hot": 4,
        "sun": 3,
        "sweating heavily": 7,
        "exhaustion": 7,
        "cramping": 6,
    }

    heat_score = 0
    detected_symptoms = []

    desc_lower = description.lower()
    for keyword, weight in heat_keywords.items():
        if keyword in desc_lower:
            heat_score += weight
            detected_symptoms.append(keyword)

    if heat_score == 0:
        return "Heat conditions manageable. Maintain hydration protocols."

    if heat_score >= 15:
        severity = "CRITICAL"
    elif heat_score >= 8:
        severity = "HIGH"
    else:
        severity = "MODERATE"

    response_parts = [f"🌡️ HEAT HAZARD DETECTED - Severity: {severity}"]
    response_parts.append(f"Symptoms/conditions: {', '.join(detected_symptoms)}")

    if severity == "CRITICAL":
        # Call 911 for potential heat stroke
        call_response = mock_911_call(
            location="Construction Site",
            emergency_type="Heat Stroke Emergency",
            description=f"Worker showing severe heat illness: {', '.join(detected_symptoms)}",
        )
        response_parts.append(f"\n✅ EMS DISPATCHED - Call ID: {call_response['call_id']}")

    # Log to safety system
    api_response = mock_safety_api_call(
        incident_type="Heat Illness",
        severity=severity,
        data={"symptoms": detected_symptoms, "heat_score": heat_score},
    )
    response_parts.append(f"\n📋 Heat incident logged: {api_response['incident_id']}")

    response_parts.append("\n❄️ COOLING PROTOCOL:")
    response_parts.append("1. Move worker to shade/air conditioning immediately")
    response_parts.append("2. Remove excess clothing and PPE")
    response_parts.append("3. Apply cool wet towels to neck, armpits, groin")
    response_parts.append("4. Provide water if conscious and able to drink")
    response_parts.append("5. Monitor vital signs every 5 minutes")
    response_parts.append("6. Do NOT return to work until cleared by medical")

    return "\n".join(response_parts)


@tool(description="Detect fall hazards and require immediate protection measures")
def detect_fall_hazard(description: str) -> str:
    fall_keywords = {
        "30 feet": 10,
        "20 feet": 9,
        "15 feet": 8,
        "10 feet": 7,
        "no guardrail": 10,
        "missing guardrail": 10,
        "unprotected edge": 9,
        "no harness": 10,
        "no fall protection": 10,
        "unstable ladder": 9,
        "scaffold": 7,
        "roof": 7,
        "floor opening": 9,
        "skylight": 8,
        "aerial lift": 6,
    }

    fall_score = 0
    detected_hazards = []

    desc_lower = description.lower()
    for keyword, weight in fall_keywords.items():
        if keyword in desc_lower:
            fall_score += weight
            detected_hazards.append(keyword)

    if fall_score == 0:
        return "No active fall hazards detected. Maintain height safety protocols."

    if fall_score >= 15:
        severity = "CRITICAL"
    elif fall_score >= 8:
        severity = "HIGH"
    else:
        severity = "MODERATE"

    response_parts = [f"⬇️ FALL HAZARD DETECTED - Severity: {severity}"]
    response_parts.append(f"Hazards identified: {', '.join(detected_hazards)}")

    # Log to safety system
    api_response = mock_safety_api_call(
        incident_type="Fall Hazard",
        severity=severity,
        data={"hazards": detected_hazards, "fall_score": fall_score},
    )
    response_parts.append(f"\n📋 Fall hazard logged: {api_response['incident_id']}")

    if severity in ["CRITICAL", "HIGH"]:
        response_parts.append("\n🛑 WORK STOPPAGE REQUIRED")
        response_parts.append("No personnel allowed in fall zone until corrected")

    response_parts.append("\n🪜 REQUIRED PROTECTION:")
    response_parts.append("1. Install guardrail system immediately (top rail, mid rail, toeboard)")
    response_parts.append("2. Provide personal fall arrest systems for all workers")
    response_parts.append("3. Inspect anchor points - minimum 5000 lb capacity")
    response_parts.append("4. Cover or barricade all floor openings")
    response_parts.append("5. Ensure ladder extends 3 feet above landing")
    response_parts.append("6. Verify 100% tie-off compliance above 6 feet")

    return "\n".join(response_parts)


def mock_sms_notification(
    message: str, urgency: str = "HIGH", incident_type: str = "Safety Alert"
) -> dict[str, Any]:
    """Mock SMS/text notification to all site personnel"""
    batch_id = f"SMS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Mock site personnel database
    site_personnel = [
        {"name": "John Smith", "role": "Safety Manager", "phone": "+1-555-0101", "priority": 1},
        {"name": "Maria Garcia", "role": "Site Supervisor", "phone": "+1-555-0102", "priority": 1},
        {"name": "David Chen", "role": "Foreman - Zone A", "phone": "+1-555-0103", "priority": 2},
        {
            "name": "Sarah Johnson",
            "role": "Foreman - Zone B",
            "phone": "+1-555-0104",
            "priority": 2,
        },
        {
            "name": "Robert Williams",
            "role": "Equipment Operator",
            "phone": "+1-555-0105",
            "priority": 3,
        },
        {
            "name": "Lisa Anderson",
            "role": "First Aid Responder",
            "phone": "+1-555-0106",
            "priority": 1,
        },
        {
            "name": "Michael Brown",
            "role": "Security Officer",
            "phone": "+1-555-0107",
            "priority": 2,
        },
        {
            "name": "Jennifer Martinez",
            "role": "Quality Inspector",
            "phone": "+1-555-0108",
            "priority": 3,
        },
        {"name": "James Davis", "role": "Crane Operator", "phone": "+1-555-0109", "priority": 2},
        {
            "name": "Patricia Wilson",
            "role": "Electrical Lead",
            "phone": "+1-555-0110",
            "priority": 2,
        },
    ]

    # Determine recipients based on urgency
    if urgency == "CRITICAL":
        recipients = site_personnel  # Everyone
    elif urgency == "HIGH":
        recipients = [p for p in site_personnel if p["priority"] <= 2]  # Supervisors and leads
    else:
        recipients = [p for p in site_personnel if p["priority"] == 1]  # Management only

    # Format message with urgency prefix
    urgency_prefix = {
        "CRITICAL": "🚨 EMERGENCY",
        "HIGH": "⚠️ URGENT",
        "MODERATE": "\u2139\ufe0f ALERT",  # information symbol
        "LOW": "📢 NOTICE",
    }

    formatted_message = f"{urgency_prefix.get(urgency, '📢')} {incident_type}: {message}"

    # Simulate sending messages
    sent_messages = []
    for person in recipients:
        sent_messages.append(
            {
                "recipient": person["name"],
                "role": person["role"],
                "phone": person["phone"],
                "status": "delivered",
                "delivery_time": datetime.now().isoformat(),
            }
        )

    response = {
        "batch_id": batch_id,
        "total_sent": len(sent_messages),
        "urgency": urgency,
        "message": formatted_message,
        "recipients": sent_messages,
        "failed": 0,
        "timestamp": datetime.now().isoformat(),
    }

    # Print notification summary
    print("\n📱 [MOCK SMS NOTIFICATION]")
    print(f"   Batch ID: {batch_id}")
    print(f"   Urgency: {urgency}")
    print(f"   Recipients: {len(sent_messages)} personnel")
    print("   Status: ALL DELIVERED")
    print("\n   Message Preview:")
    print(f"   \"{formatted_message[:80]}{'...' if len(formatted_message) > 80 else ''}\"")
    print("\n   Sent to:")
    for msg in sent_messages[:5]:  # Show first 5
        print(f"   • {msg['recipient']} ({msg['role']}) - {msg['phone']}")
    if len(sent_messages) > 5:
        print(f"   • ... and {len(sent_messages) - 5} more personnel")

    return response


@tool(description="Send SMS text notification to all site personnel about safety hazard")
def send_site_alert(alert_message: str, urgency_level: str = "HIGH") -> str:
    """
    Send text message alert to all construction site personnel

    Args:
        alert_message: The safety alert message to send
        urgency_level: CRITICAL, HIGH, MODERATE, or LOW

    Returns:
        Confirmation of messages sent
    """
    # Send SMS notification
    sms_response = mock_sms_notification(
        message=alert_message, urgency=urgency_level, incident_type="SITE SAFETY ALERT"
    )

    result = [
        "✅ SITE-WIDE ALERT SENT",
        f"Batch ID: {sms_response['batch_id']}",
        f"Total Recipients: {sms_response['total_sent']} personnel",
        "Delivery Status: ALL DELIVERED",
        f'\nMessage sent: "{alert_message}"',
    ]

    return "\n".join(result)
