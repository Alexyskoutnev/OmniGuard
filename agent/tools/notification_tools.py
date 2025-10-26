"""
Shared notification and mock service tools
"""

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

    return response


def mock_safety_api_call(incident_type: str, severity: str, data: dict[str, Any]) -> dict[str, Any]:
    """Mock call to external safety management API"""
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

    return response


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

    return response


@tool(description="Send SMS text notification to all site personnel about safety hazard")
def send_site_alert(alert_message: str, urgency_level: str = "HIGH") -> str:
    sms_response = mock_sms_notification(
        message=alert_message, urgency=urgency_level, incident_type="SITE SAFETY ALERT"
    )

    result = [
        "SITE-WIDE ALERT SENT",
        f"Batch ID: {sms_response['batch_id']}",
        f"Total Recipients: {sms_response['total_sent']} personnel",
        "Delivery Status: ALL DELIVERED",
        f'\nMessage sent: "{alert_message}"',
    ]

    return "\n".join(result)
