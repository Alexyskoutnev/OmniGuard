"""
Tiered Approval Engine for Safety Actions

Implements approval workflows based on risk levels and action types.
- Auto-execute: Low-risk actions (notifications, logging)
- Human approval: Medium/high-risk actions (alarms, work stoppage)
- Emergency protocols: Special handling for critical situations
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """Status of approval requests."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    AUTO_APPROVED = "auto_approved"


class RiskLevel(Enum):
    """Risk levels for actions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ApprovalRequest:
    """Request for action approval."""
    request_id: str
    action_type: str
    description: str
    priority: str
    risk_level: RiskLevel
    parameters: Dict[str, Any]
    requester: str
    requested_at: datetime
    expires_at: datetime
    approver_role: str


@dataclass
class ApprovalResult:
    """Result of approval process."""
    request_id: str
    approved: bool
    status: ApprovalStatus
    approver: Optional[str] = None
    approved_at: Optional[datetime] = None
    reason: Optional[str] = None
    auto_approved: bool = False


class TieredApprovalManager:
    """
    Manages tiered approval system for safety actions.

    Approval tiers:
    1. Auto-approve: Low-risk notifications, logging, information preparation
    2. Supervisor approval: Medium-risk site control, equipment actions
    3. Management approval: High-risk work stoppage, evacuation
    4. Emergency bypass: Critical situations with post-action review
    """

    def __init__(self):
        # Auto-approval rules
        self.auto_approve_actions = {
            "send_sms_blast",
            "send_email_alert",
            "notify_slack_teams",
            "prepare_emergency_info",
            "prepare_phone_call_info",
            "log_incident",
            "schedule_follow_up"
        }

        # Approval requirements by action type
        self.approval_rules = {
            "trigger_site_alarm": {
                "risk_level": RiskLevel.MEDIUM,
                "approver_role": "site_supervisor",
                "timeout_minutes": 5
            },
            "broadcast_announcement": {
                "risk_level": RiskLevel.MEDIUM,
                "approver_role": "site_supervisor",
                "timeout_minutes": 3
            },
            "stop_work_immediately": {
                "risk_level": RiskLevel.HIGH,
                "approver_role": "safety_manager",
                "timeout_minutes": 2
            },
            "evacuate_area": {
                "risk_level": RiskLevel.HIGH,
                "approver_role": "safety_manager",
                "timeout_minutes": 1
            }
        }

        # Emergency bypass rules (auto-approve critical situations)
        self.emergency_bypass_conditions = {
            "medical_emergency": ["prepare_emergency_info", "trigger_site_alarm", "broadcast_announcement"],
            "imminent_danger": ["stop_work_immediately", "trigger_site_alarm", "evacuate_area"],
            "injury_occurred": ["prepare_emergency_info", "trigger_site_alarm"]
        }

        # Active approval requests
        self.pending_requests: Dict[str, ApprovalRequest] = {}
        self.approval_history: List[ApprovalResult] = []

        # Mock approver system (in production, integrate with actual approval system)
        self.mock_approvers = {
            "site_supervisor": True,  # Always approves for demo
            "safety_manager": True,
            "emergency_coordinator": True
        }

    async def request_approval(
        self,
        action_type: str,
        description: str,
        priority: str,
        parameters: Dict[str, Any]
    ) -> ApprovalResult:
        """
        Request approval for an action.

        Args:
            action_type: Type of action requiring approval
            description: Human-readable description of the action
            priority: Priority level (low, medium, high, critical)
            parameters: Action parameters for context

        Returns:
            ApprovalResult indicating if action is approved
        """

        # Check for auto-approval
        if action_type in self.auto_approve_actions:
            return self._create_auto_approval_result(action_type, description)

        # Check for emergency bypass
        emergency_result = self._check_emergency_bypass(action_type, parameters, priority)
        if emergency_result:
            return emergency_result

        # Create approval request
        request = self._create_approval_request(action_type, description, priority, parameters)

        # Process approval based on rules
        if action_type in self.approval_rules:
            return await self._process_approval_request(request)
        else:
            # Unknown action - default to requiring approval
            return await self._process_unknown_action_request(request)

    def _create_auto_approval_result(self, action_type: str, description: str) -> ApprovalResult:
        """Create auto-approval result for low-risk actions."""
        request_id = f"auto_{action_type}_{int(datetime.now().timestamp())}"

        result = ApprovalResult(
            request_id=request_id,
            approved=True,
            status=ApprovalStatus.AUTO_APPROVED,
            approver="system",
            approved_at=datetime.now(),
            reason=f"Auto-approved: {action_type} is low-risk",
            auto_approved=True
        )

        self.approval_history.append(result)
        logger.info(f"Auto-approved action: {action_type}")
        return result

    def _check_emergency_bypass(
        self,
        action_type: str,
        parameters: Dict[str, Any],
        priority: str
    ) -> Optional[ApprovalResult]:
        """Check if action qualifies for emergency bypass."""

        # Check priority level
        if priority.lower() == "critical":
            # Critical priority actions get emergency bypass
            request_id = f"emergency_{action_type}_{int(datetime.now().timestamp())}"

            result = ApprovalResult(
                request_id=request_id,
                approved=True,
                status=ApprovalStatus.AUTO_APPROVED,
                approver="emergency_system",
                approved_at=datetime.now(),
                reason="Emergency bypass due to critical priority",
                auto_approved=True
            )

            self.approval_history.append(result)
            logger.warning(f"Emergency bypass approved for critical action: {action_type}")
            return result

        # Check for specific emergency conditions
        incident_type = parameters.get('incident_type', '').lower()
        description = parameters.get('description', '').lower()

        for condition, allowed_actions in self.emergency_bypass_conditions.items():
            if condition in incident_type or condition in description:
                if action_type in allowed_actions:
                    request_id = f"emergency_{condition}_{int(datetime.now().timestamp())}"

                    result = ApprovalResult(
                        request_id=request_id,
                        approved=True,
                        status=ApprovalStatus.AUTO_APPROVED,
                        approver="emergency_system",
                        approved_at=datetime.now(),
                        reason=f"Emergency bypass: {condition} detected",
                        auto_approved=True
                    )

                    self.approval_history.append(result)
                    logger.warning(f"Emergency bypass approved for {condition}: {action_type}")
                    return result

        return None

    def _create_approval_request(
        self,
        action_type: str,
        description: str,
        priority: str,
        parameters: Dict[str, Any]
    ) -> ApprovalRequest:
        """Create approval request object."""

        rules = self.approval_rules.get(action_type, {
            "risk_level": RiskLevel.MEDIUM,
            "approver_role": "site_supervisor",
            "timeout_minutes": 5
        })

        request_id = f"req_{action_type}_{int(datetime.now().timestamp())}"
        now = datetime.now()
        expires_at = now + timedelta(minutes=rules["timeout_minutes"])

        return ApprovalRequest(
            request_id=request_id,
            action_type=action_type,
            description=description,
            priority=priority,
            risk_level=rules["risk_level"],
            parameters=parameters,
            requester="safety_agent",
            requested_at=now,
            expires_at=expires_at,
            approver_role=rules["approver_role"]
        )

    async def _process_approval_request(self, request: ApprovalRequest) -> ApprovalResult:
        """Process approval request with timeout."""

        self.pending_requests[request.request_id] = request
        logger.info(f"Approval requested: {request.request_id} for {request.action_type}")

        try:
            # In production, this would integrate with actual approval system
            # For demo, we simulate approval process
            approval_granted = await self._simulate_approval_process(request)

            if approval_granted:
                result = ApprovalResult(
                    request_id=request.request_id,
                    approved=True,
                    status=ApprovalStatus.APPROVED,
                    approver=request.approver_role,
                    approved_at=datetime.now(),
                    reason=f"Approved by {request.approver_role}"
                )
            else:
                result = ApprovalResult(
                    request_id=request.request_id,
                    approved=False,
                    status=ApprovalStatus.DENIED,
                    reason="Action denied by approver"
                )

        except asyncio.TimeoutError:
            result = ApprovalResult(
                request_id=request.request_id,
                approved=False,
                status=ApprovalStatus.EXPIRED,
                reason="Approval request timed out"
            )

        # Clean up
        self.pending_requests.pop(request.request_id, None)
        self.approval_history.append(result)

        logger.info(f"Approval result: {request.request_id} = {result.status.value}")
        return result

    async def _process_unknown_action_request(self, request: ApprovalRequest) -> ApprovalResult:
        """Process request for unknown action type."""

        # Unknown actions default to requiring approval
        logger.warning(f"Unknown action type requiring approval: {request.action_type}")

        return ApprovalResult(
            request_id=request.request_id,
            approved=False,
            status=ApprovalStatus.DENIED,
            reason=f"Unknown action type: {request.action_type}"
        )

    async def _simulate_approval_process(self, request: ApprovalRequest) -> bool:
        """Simulate approval process (replace with real integration)."""

        # Simulate processing delay
        delay = min(request.risk_level.value.count('h') + 1, 3)  # 1-3 seconds based on risk
        await asyncio.sleep(delay)

        # Mock approval decision based on approver role
        return self.mock_approvers.get(request.approver_role, False)

    def get_pending_requests(self) -> List[ApprovalRequest]:
        """Get all pending approval requests."""
        now = datetime.now()

        # Remove expired requests
        expired_ids = [
            req_id for req_id, req in self.pending_requests.items()
            if req.expires_at < now
        ]

        for req_id in expired_ids:
            expired_req = self.pending_requests.pop(req_id)
            self.approval_history.append(
                ApprovalResult(
                    request_id=req_id,
                    approved=False,
                    status=ApprovalStatus.EXPIRED,
                    reason="Request expired"
                )
            )

        return list(self.pending_requests.values())

    def get_approval_history(self, limit: int = 100) -> List[ApprovalResult]:
        """Get recent approval history."""
        return self.approval_history[-limit:]

    def get_approval_stats(self) -> Dict[str, Any]:
        """Get approval system statistics."""
        if not self.approval_history:
            return {"total": 0, "approved": 0, "denied": 0, "auto_approved": 0}

        total = len(self.approval_history)
        approved = sum(1 for r in self.approval_history if r.approved)
        auto_approved = sum(1 for r in self.approval_history if r.auto_approved)
        denied = total - approved

        return {
            "total_requests": total,
            "approved": approved,
            "denied": denied,
            "auto_approved": auto_approved,
            "approval_rate": approved / total if total > 0 else 0,
            "auto_approval_rate": auto_approved / total if total > 0 else 0,
            "pending": len(self.pending_requests)
        }