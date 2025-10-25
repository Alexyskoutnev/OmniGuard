"""
Safety Agent Orchestrator

Main orchestrator that coordinates the agentic brain, MCP tools, and approval systems
to execute intelligent safety responses based on video analysis.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.agentic_brain import nemotron_brain, SimpleSafetyInput, ActionPlan, AgentAction
from src.agents.mcp_tools import safety_mcp_server
from src.agents.approval.approval_engine import TieredApprovalManager

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of action execution."""
    action: AgentAction
    success: bool
    result: Any
    execution_time: float
    error_message: Optional[str] = None
    approval_status: str = "not_required"  # not_required, pending, approved, denied


@dataclass
class SafetyResponse:
    """Complete response from safety agent system."""
    video_id: str
    plan_id: str
    safety_input: SimpleSafetyInput
    action_plan: ActionPlan
    execution_results: List[ExecutionResult]
    total_execution_time: float
    overall_success: bool
    timestamp: str


class SafetyAgentOrchestrator:
    """
    Main orchestrator for the safety agent system.

    Coordinates between:
    1. Agentic brain (Nemotron) for decision making
    2. MCP tools for action execution
    3. Approval system for high-risk actions
    4. Logging and audit trail
    """

    def __init__(self):
        self.brain = nemotron_brain
        self.mcp_server = safety_mcp_server
        self.approval_manager = TieredApprovalManager()

        # Execution statistics
        self.stats = {
            "total_responses": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "actions_executed": 0,
            "actions_requiring_approval": 0,
            "avg_response_time": 0.0
        }

    async def initialize(self):
        """Initialize the safety agent system."""
        logger.info("Initializing Safety Agent Orchestrator...")

        # Load the brain model
        await self._load_brain()

        # Initialize MCP server (if needed)
        # Note: In production, MCP server might run separately

        logger.info("Safety Agent Orchestrator initialized successfully")

    async def process_safety_input(self, safety_input_dict: Dict[str, Any]) -> SafetyResponse:
        """
        Process safety input and execute intelligent response.

        Args:
            safety_input_dict: Dictionary with video_id, safety_status, scene_description, etc.

        Returns:
            SafetyResponse with execution results
        """
        start_time = asyncio.get_event_loop().time()
        self.stats["total_responses"] += 1

        try:
            # Parse input
            safety_input = self._parse_safety_input(safety_input_dict)

            # Create action plan using brain
            action_plan = await self.brain.create_action_plan(safety_input)

            # Execute action plan
            execution_results = await self._execute_action_plan(action_plan)

            # Calculate metrics
            execution_time = asyncio.get_event_loop().time() - start_time
            overall_success = all(result.success for result in execution_results)

            if overall_success:
                self.stats["successful_responses"] += 1
            else:
                self.stats["failed_responses"] += 1

            # Update average response time
            total_time = self.stats["avg_response_time"] * (self.stats["total_responses"] - 1)
            self.stats["avg_response_time"] = (total_time + execution_time) / self.stats["total_responses"]

            safety_response = SafetyResponse(
                video_id=safety_input.video_id,
                plan_id=action_plan.plan_id,
                safety_input=safety_input,
                action_plan=action_plan,
                execution_results=execution_results,
                total_execution_time=execution_time,
                overall_success=overall_success,
                timestamp=datetime.now().isoformat()
            )

            logger.info(f"Safety response completed for {safety_input.video_id}: "
                       f"success={overall_success}, time={execution_time:.2f}s")

            return safety_response

        except Exception as e:
            logger.error(f"Safety processing failed: {str(e)}")
            self.stats["failed_responses"] += 1

            # Return error response
            return SafetyResponse(
                video_id=safety_input_dict.get('video_id', 'unknown'),
                plan_id="error_plan",
                safety_input=self._create_empty_safety_input(),
                action_plan=self._create_error_action_plan(str(e)),
                execution_results=[],
                total_execution_time=asyncio.get_event_loop().time() - start_time,
                overall_success=False,
                timestamp=datetime.now().isoformat()
            )

    async def _execute_action_plan(self, action_plan: ActionPlan) -> List[ExecutionResult]:
        """Execute the action plan with proper approval handling."""
        execution_results = []

        if action_plan.execution_strategy == "parallel":
            # Execute actions in parallel (for independent actions)
            tasks = []
            for action in action_plan.actions:
                tasks.append(self._execute_single_action(action))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            execution_results = [r for r in results if isinstance(r, ExecutionResult)]

        else:  # sequential or conditional
            # Execute actions one by one
            for action in action_plan.actions:
                result = await self._execute_single_action(action)
                execution_results.append(result)

                # For conditional execution, stop on failure
                if action_plan.execution_strategy == "conditional" and not result.success:
                    logger.warning(f"Stopping execution due to failure in action: {action.tool_name}")
                    break

        self.stats["actions_executed"] += len(execution_results)
        return execution_results

    async def _execute_single_action(self, action: AgentAction) -> ExecutionResult:
        """Execute a single action with approval handling."""
        start_time = asyncio.get_event_loop().time()

        try:
            # Check if approval is required
            if action.requires_approval:
                self.stats["actions_requiring_approval"] += 1
                approval_result = await self.approval_manager.request_approval(
                    action_type=action.tool_name,
                    description=action.reasoning,
                    priority=action.priority,
                    parameters=action.parameters
                )

                if not approval_result.approved:
                    return ExecutionResult(
                        action=action,
                        success=False,
                        result=None,
                        execution_time=asyncio.get_event_loop().time() - start_time,
                        approval_status="denied",
                        error_message="Action denied by approval system"
                    )

            # Execute the action using MCP tools
            tool_result = await self._call_mcp_tool(action.tool_name, action.parameters)

            execution_time = asyncio.get_event_loop().time() - start_time

            return ExecutionResult(
                action=action,
                success=True,
                result=tool_result,
                execution_time=execution_time,
                approval_status="approved" if action.requires_approval else "not_required"
            )

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            logger.error(f"Action execution failed for {action.tool_name}: {str(e)}")

            return ExecutionResult(
                action=action,
                success=False,
                result=None,
                execution_time=execution_time,
                error_message=str(e)
            )

    async def _call_mcp_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Call MCP tool with given parameters."""
        # Get the tool method from the MCP server
        if hasattr(self.mcp_server.mcp, 'tools') and tool_name in self.mcp_server.mcp.tools:
            tool_func = self.mcp_server.mcp.tools[tool_name]
            return await tool_func(**parameters)
        else:
            # Fallback: call the method directly if it exists
            method_name = f"_{tool_name}"
            if hasattr(self.mcp_server, method_name):
                method = getattr(self.mcp_server, method_name)
                return await method(**parameters)
            else:
                raise ValueError(f"MCP tool not found: {tool_name}")

    def _parse_safety_input(self, input_dict: Dict[str, Any]) -> SimpleSafetyInput:
        """Parse input dictionary into SimpleSafetyInput."""
        return SimpleSafetyInput(
            video_id=input_dict['video_id'],
            safety_status=input_dict['safety_status'],
            scene_description=input_dict['scene_description'],
            predictions=input_dict['predictions'],
            safety_response=input_dict['safety_response']
        )

    def _create_empty_safety_input(self) -> SimpleSafetyInput:
        """Create empty safety input for error cases."""
        return SimpleSafetyInput(
            video_id="unknown",
            safety_status="UNKNOWN",
            scene_description="Error processing input",
            predictions={"probability": 0, "incident_type": "unknown"},
            safety_response="Error occurred"
        )

    def _create_error_action_plan(self, error_message: str) -> ActionPlan:
        """Create error action plan."""
        return ActionPlan(
            plan_id="error_plan",
            description=f"Error plan: {error_message}",
            actions=[],
            total_confidence=0.0,
            execution_strategy="sequential"
        )

    async def _load_brain(self):
        """Load the agentic brain model."""
        try:
            self.brain.load_model()
            logger.info("Agentic brain loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load agentic brain: {str(e)}")
            # Continue without brain - will use fallback logic
            logger.warning("Continuing with fallback logic only")

    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics."""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_responses"] / self.stats["total_responses"]
                if self.stats["total_responses"] > 0 else 0
            ),
            "approval_rate": (
                self.stats["actions_requiring_approval"] / self.stats["actions_executed"]
                if self.stats["actions_executed"] > 0 else 0
            )
        }

    async def batch_process(self, safety_inputs: List[Dict[str, Any]]) -> List[SafetyResponse]:
        """Process multiple safety inputs in batch."""
        logger.info(f"Processing batch of {len(safety_inputs)} safety inputs")

        tasks = [self.process_safety_input(input_dict) for input_dict in safety_inputs]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return only successful results
        safety_responses = [r for r in results if isinstance(r, SafetyResponse)]

        logger.info(f"Batch processing completed: {len(safety_responses)} responses")
        return safety_responses


# Global orchestrator instance
safety_orchestrator = SafetyAgentOrchestrator()