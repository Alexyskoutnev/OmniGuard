"""
MCP Tool Registry using FastMCP for Construction Safety Agents

Defines MCP tools for each safety action type using the FastMCP library
for proper MCP protocol implementation.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time
import logging
from datetime import datetime
import asyncio

from fastmcp import FastMCP

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for tool execution authorization."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SafetyActionRequest:
    """Request for safety action execution."""
    action_type: str
    incident_type: str
    risk_level: RiskLevel
    description: str
    location: str
    workers_affected: int
    timestamp: str


class SafetyMCPServer:
    """MCP Server for construction safety tools using FastMCP."""

    def __init__(self):
        self.mcp = FastMCP("Construction Safety Agent")
        self._register_tools()

    def _register_tools(self):
        """Register all safety-related MCP tools."""

        @self.mcp.tool()
        async def send_sms_blast(
            recipients: List[str],
            message: str,
            priority: str = "normal"
        ) -> Dict[str, Any]:
            """
            Send SMS blast to workers and supervisors.

            Args:
                recipients: List of phone numbers to send SMS to
                message: SMS message content
                priority: Message priority (normal, urgent, critical)

            Returns:
                Result with number of messages sent and message ID
            """
            logger.info(f"SMS blast to {len(recipients)} recipients: {message[:50]}...")

            # Placeholder implementation - integrate with Twilio/AWS SNS
            return {
                "sent": len(recipients),
                "message_id": f"sms_{int(time.time())}",
                "priority": priority,
                "timestamp": datetime.now().isoformat()
            }

        @self.mcp.tool()
        async def send_email_alert(
            recipients: List[str],
            subject: str,
            body: str,
            priority: str = "normal"
        ) -> Dict[str, Any]:
            """
            Send email alert to management and safety officers.

            Args:
                recipients: List of email addresses
                subject: Email subject line
                body: Email body content
                priority: Email priority level

            Returns:
                Result with number of emails sent and message ID
            """
            logger.info(f"Email alert to {len(recipients)} recipients: {subject}")

            # Placeholder implementation - integrate with SendGrid/AWS SES
            return {
                "sent": len(recipients),
                "message_id": f"email_{int(time.time())}",
                "subject": subject,
                "timestamp": datetime.now().isoformat()
            }

        @self.mcp.tool()
        async def notify_slack_teams(
            channels: List[str],
            message: str,
            priority: str = "normal"
        ) -> Dict[str, Any]:
            """
            Send notification to Slack/Teams channels.

            Args:
                channels: List of channel names or IDs
                message: Message content
                priority: Message priority level

            Returns:
                Result with number of channels notified
            """
            logger.info(f"Slack/Teams notification to {len(channels)} channels")

            # Placeholder implementation - integrate with Slack/Teams APIs
            return {
                "sent": len(channels),
                "message_id": f"chat_{int(time.time())}",
                "channels": channels,
                "timestamp": datetime.now().isoformat()
            }

        @self.mcp.tool()
        async def prepare_emergency_info(
            incident_type: str,
            location: str,
            description: str,
            workers_affected: int
        ) -> Dict[str, Any]:
            """
            Prepare emergency service information package (does not call 911).

            Args:
                incident_type: Type of incident (fall, injury, etc.)
                location: Specific location on site
                description: Detailed description of incident
                workers_affected: Number of workers involved

            Returns:
                Formatted emergency information package for human operator
            """
            emergency_info = {
                "incident_type": incident_type,
                "location": location,
                "description": description,
                "workers_affected": workers_affected,
                "timestamp": datetime.now().isoformat(),
                "contact_info": "Site Supervisor: [SITE_SUPERVISOR_PHONE]",
                "emergency_number": "911",
                "prepared_by": "Safety AI Agent",
                "instructions": "Human operator should call 911 with this information"
            }

            logger.info(f"Emergency information prepared for {incident_type} at {location}")
            return emergency_info

        @self.mcp.tool()
        async def prepare_phone_call_info(
            call_type: str,
            recipient: str,
            message: str
        ) -> Dict[str, Any]:
            """
            Prepare phone call information for human operator.

            Args:
                call_type: Type of call (supervisor, management, emergency)
                recipient: Who to call (name/role)
                message: Key points to communicate

            Returns:
                Formatted call information for human execution
            """
            call_info = {
                "call_type": call_type,
                "recipient": recipient,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "prepared_by": "Safety AI Agent",
                "instructions": "Human operator should make this call immediately"
            }

            logger.info(f"Phone call info prepared for {recipient}")
            return call_info

        @self.mcp.tool()
        async def trigger_site_alarm(
            alarm_type: str = "safety",
            message: str = "Safety alert"
        ) -> Dict[str, Any]:
            """
            Trigger site-wide safety alarm system.

            Args:
                alarm_type: Type of alarm (safety, evacuation, emergency)
                message: Optional message for announcement

            Returns:
                Confirmation of alarm activation
            """
            logger.info(f"Site alarm triggered: {alarm_type} - {message}")

            # Placeholder implementation - integrate with site alarm system
            return {
                "alarm_triggered": True,
                "type": alarm_type,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }

        @self.mcp.tool()
        async def broadcast_announcement(
            message: str,
            priority: str = "normal"
        ) -> Dict[str, Any]:
            """
            Broadcast safety announcement over PA system.

            Args:
                message: Announcement message
                priority: Priority level (normal, urgent, emergency)

            Returns:
                Confirmation of broadcast
            """
            logger.info(f"PA announcement: {message[:50]}...")

            # Placeholder implementation - integrate with PA system
            return {
                "announced": True,
                "message": message,
                "priority": priority,
                "timestamp": datetime.now().isoformat()
            }

        @self.mcp.tool()
        async def request_approval(
            action: str,
            risk_level: str,
            description: str,
            approver: str
        ) -> Dict[str, Any]:
            """
            Request approval for medium/high-risk actions.

            Args:
                action: Action requiring approval
                risk_level: Risk level of action
                description: Detailed description
                approver: Who should approve

            Returns:
                Approval request ID and status
            """
            approval_id = f"approval_{action}_{int(time.time())}"
            logger.info(f"Approval requested: {approval_id} for {action}")

            return {
                "approval_id": approval_id,
                "status": "pending",
                "approver": approver,
                "action": action,
                "risk_level": risk_level,
                "timestamp": datetime.now().isoformat()
            }

        @self.mcp.tool()
        async def log_incident(
            incident_id: str,
            incident_type: str,
            description: str,
            actions_taken: List[str]
        ) -> Dict[str, Any]:
            """
            Log safety incident for audit trail and compliance.

            Args:
                incident_id: Unique incident identifier
                incident_type: Type of safety incident
                description: Detailed incident description
                actions_taken: List of actions taken in response

            Returns:
                Confirmation of logged incident
            """
            log_entry = {
                "incident_id": incident_id,
                "incident_type": incident_type,
                "description": description,
                "actions_taken": actions_taken,
                "timestamp": datetime.now().isoformat(),
                "logged_by": "Safety AI Agent"
            }

            logger.info(f"Incident logged: {incident_id}")
            return log_entry

        @self.mcp.tool()
        async def schedule_follow_up(
            action_type: str,
            timeline: str,
            responsible_party: str,
            description: str
        ) -> Dict[str, Any]:
            """
            Schedule follow-up safety actions.

            Args:
                action_type: Type of follow-up action
                timeline: When action should be completed
                responsible_party: Who is responsible
                description: Description of required action

            Returns:
                Scheduled task information
            """
            task_id = f"task_{action_type}_{int(time.time())}"

            return {
                "task_id": task_id,
                "action_type": action_type,
                "timeline": timeline,
                "responsible_party": responsible_party,
                "description": description,
                "status": "scheduled",
                "timestamp": datetime.now().isoformat()
            }

    async def run_server(self, transport="stdio"):
        """Run the MCP server."""
        await self.mcp.run(transport)


# Global MCP server instance
safety_mcp_server = SafetyMCPServer()