"""
Agentic Brain using NVIDIA Nemotron-Nano-9B-v2

This module provides the intelligent decision-making component for the safety agent system.
It takes simplified safety analysis inputs and makes intelligent decisions about tool usage
and orchestrates multi-step safety response workflows.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig

# Add project root to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)


@dataclass
class SimpleSafetyInput:
    """Simplified safety input format."""
    video_id: str
    safety_status: str  # LOW, MEDIUM, HIGH, CRITICAL
    scene_description: str
    predictions: Dict[str, Any]  # probability, incident_type
    safety_response: str  # Natural language response


@dataclass
class AgentAction:
    """Single action to be executed by an agent."""
    tool_name: str
    parameters: Dict[str, Any]
    reasoning: str
    confidence: float
    priority: str  # low, medium, high, critical
    requires_approval: bool
    estimated_duration: str  # immediate, minutes, hours


@dataclass
class ActionPlan:
    """Multi-step action plan for safety response."""
    plan_id: str
    description: str
    actions: List[AgentAction]
    total_confidence: float
    execution_strategy: str  # sequential, parallel, conditional


class NemotronAgenticBrain:
    """
    Agentic brain using NVIDIA Nemotron-Nano-9B-v2 for intelligent safety decision making.

    Takes simplified safety inputs and creates executable action plans using available MCP tools.
    """

    def __init__(self, model_path: str = None):
        self.model_path = model_path or str(Path(__file__).parent.parent / "models" / "NVIDIA-Nemotron-Nano-9B-v2")
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Available MCP tools
        self.available_tools = {
            "send_sms_blast": "Send urgent SMS to workers and supervisors",
            "send_email_alert": "Send detailed email alerts to management",
            "notify_slack_teams": "Send real-time notifications to team channels",
            "prepare_emergency_info": "Prepare emergency service information package",
            "prepare_phone_call_info": "Prepare urgent phone call information",
            "trigger_site_alarm": "Activate site-wide safety alarms",
            "broadcast_announcement": "Make PA announcements to all workers",
            "request_approval": "Request approval for high-risk actions",
            "log_incident": "Log incident for compliance and audit",
            "schedule_follow_up": "Schedule follow-up safety actions"
        }

    def load_model(self):
        """Load the Nemotron model for agentic decision making."""
        logger.info(f"Loading Nemotron brain model from: {self.model_path}")

        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16,
                device_map="auto"
            )

            logger.info("Nemotron brain model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load Nemotron brain model: {str(e)}")
            raise

    async def create_action_plan(self, safety_input: SimpleSafetyInput) -> ActionPlan:
        """
        Create intelligent action plan based on safety input.

        Args:
            safety_input: Simplified safety analysis input

        Returns:
            ActionPlan with intelligent tool selection and execution strategy
        """

        # Create prompt for the brain
        prompt = self._create_decision_prompt(safety_input)

        # Get brain's decision
        brain_response = await self._query_brain(prompt)

        # Parse response into action plan
        action_plan = self._parse_brain_response(brain_response, safety_input)

        logger.info(f"Brain created action plan: {action_plan.plan_id} with {len(action_plan.actions)} actions")
        return action_plan

    def _create_decision_prompt(self, safety_input: SimpleSafetyInput) -> str:
        """Create decision prompt for the brain."""

        tools_list = "\n".join([f"- {name}: {desc}" for name, desc in self.available_tools.items()])

        return f"""You are an intelligent safety agent for construction sites. Analyze this safety situation and create an optimal action plan.

SAFETY SITUATION:
Video ID: {safety_input.video_id}
Safety Status: {safety_input.safety_status}
Scene: {safety_input.scene_description}
Prediction: {safety_input.predictions.get('incident_type', 'Unknown')} (probability: {safety_input.predictions.get('probability', 0)})
Recommended Response: {safety_input.safety_response}

AVAILABLE TOOLS:
{tools_list}

DECISION FRAMEWORK:
- CRITICAL/HIGH: Immediate action, multiple channels, emergency protocols
- MEDIUM: Prompt action, supervisory notification, monitoring
- LOW: Standard procedures, logging, scheduled follow-up

APPROVAL REQUIREMENTS:
- Auto-execute: Notifications, logging, emergency info preparation
- Requires approval: Site alarms, work stoppage, equipment control

Create an action plan with specific tools and parameters. Consider:
1. Urgency based on safety status and prediction probability
2. Communication strategy (who needs to know, how quickly)
3. Emergency protocols if needed
4. Follow-up and documentation requirements

Respond with JSON:
{{
    "plan_id": "unique_plan_id",
    "description": "Brief plan description",
    "total_confidence": 0.85,
    "execution_strategy": "sequential|parallel|conditional",
    "actions": [
        {{
            "tool_name": "tool_name",
            "parameters": {{
                "key": "value"
            }},
            "reasoning": "Why this action",
            "confidence": 0.9,
            "priority": "critical|high|medium|low",
            "requires_approval": false,
            "estimated_duration": "immediate|minutes|hours"
        }}
    ]
}}"""

    async def _query_brain(self, prompt: str) -> str:
        """Query the Nemotron brain model."""
        if self.model is None:
            raise RuntimeError("Brain model not loaded. Call load_model() first.")

        try:
            # Prepare input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=4096,
                padding=True
            ).to(self.device)

            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1024,
                    temperature=0.2,  # Low temperature for consistent decisions
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode response
            generated_text = self.tokenizer.decode(
                outputs[0][inputs.input_ids.shape[1]:],
                skip_special_tokens=True
            )

            return generated_text.strip()

        except Exception as e:
            logger.error(f"Brain query failed: {str(e)}")
            raise

    def _parse_brain_response(self, response: str, safety_input: SimpleSafetyInput) -> ActionPlan:
        """Parse brain response into structured action plan."""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                plan_data = json.loads(json_str)

                actions = [
                    AgentAction(
                        tool_name=action['tool_name'],
                        parameters=action['parameters'],
                        reasoning=action['reasoning'],
                        confidence=action['confidence'],
                        priority=action['priority'],
                        requires_approval=action['requires_approval'],
                        estimated_duration=action['estimated_duration']
                    )
                    for action in plan_data['actions']
                ]

                return ActionPlan(
                    plan_id=plan_data['plan_id'],
                    description=plan_data['description'],
                    actions=actions,
                    total_confidence=plan_data['total_confidence'],
                    execution_strategy=plan_data['execution_strategy']
                )

        except Exception as e:
            logger.warning(f"Failed to parse brain response: {str(e)}")

        # Fallback: Create rule-based plan
        return self._create_fallback_plan(safety_input)

    def _create_fallback_plan(self, safety_input: SimpleSafetyInput) -> ActionPlan:
        """Create fallback action plan using rule-based logic."""
        actions = []
        safety_status = safety_input.safety_status.upper()
        incident_type = safety_input.predictions.get('incident_type', '').lower()
        probability = safety_input.predictions.get('probability', 0)

        # Rule-based action selection
        if safety_status in ['CRITICAL', 'HIGH'] or probability > 0.8:
            # Emergency situation
            if 'medical' in incident_type or 'injury' in incident_type:
                actions.append(
                    AgentAction(
                        tool_name="prepare_emergency_info",
                        parameters={
                            "incident_type": incident_type,
                            "location": "construction_site",
                            "description": safety_input.scene_description,
                            "workers_affected": 1
                        },
                        reasoning="Medical emergency requires immediate EMS preparation",
                        confidence=0.9,
                        priority="critical",
                        requires_approval=False,
                        estimated_duration="immediate"
                    )
                )

            # Immediate notifications
            actions.append(
                AgentAction(
                    tool_name="send_sms_blast",
                    parameters={
                        "recipients": ["site_supervisor", "safety_officer", "management"],
                        "message": f"URGENT: {incident_type} detected. {safety_input.scene_description[:100]}",
                        "priority": "critical"
                    },
                    reasoning="Critical situation requires immediate notification",
                    confidence=0.85,
                    priority="critical",
                    requires_approval=False,
                    estimated_duration="immediate"
                )
            )

            # Site alarm for high-risk situations
            if probability > 0.9:
                actions.append(
                    AgentAction(
                        tool_name="trigger_site_alarm",
                        parameters={
                            "alarm_type": "emergency",
                            "message": f"Emergency alert: {incident_type}"
                        },
                        reasoning="High probability incident requires site-wide alert",
                        confidence=0.8,
                        priority="high",
                        requires_approval=True,
                        estimated_duration="immediate"
                    )
                )

        elif safety_status == 'MEDIUM':
            # Standard notification
            actions.append(
                AgentAction(
                    tool_name="notify_slack_teams",
                    parameters={
                        "channels": ["safety_team", "site_management"],
                        "message": f"Safety alert: {safety_input.scene_description}",
                        "priority": "medium"
                    },
                    reasoning="Medium risk requires team notification",
                    confidence=0.7,
                    priority="medium",
                    requires_approval=False,
                    estimated_duration="immediate"
                )
            )

        # Always log incident
        actions.append(
            AgentAction(
                tool_name="log_incident",
                parameters={
                    "incident_id": safety_input.video_id,
                    "incident_type": incident_type,
                    "description": safety_input.scene_description,
                    "actions_taken": [action.tool_name for action in actions]
                },
                reasoning="All incidents must be logged for compliance",
                confidence=0.95,
                priority="low",
                requires_approval=False,
                estimated_duration="immediate"
            )
        )

        return ActionPlan(
            plan_id=f"fallback_{safety_input.video_id}",
            description=f"Fallback plan for {safety_status} safety situation",
            actions=actions,
            total_confidence=0.7,
            execution_strategy="sequential"
        )


# Global brain instance
nemotron_brain = NemotronAgenticBrain()