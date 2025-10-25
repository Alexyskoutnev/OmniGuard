#!/usr/bin/env python3
"""
Example usage of the Construction Safety Agent System

This script demonstrates how to use the agentic system with the simplified
safety input format to automatically execute safety responses.
"""

import asyncio
import json
import logging
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.agents.safety_agent import safety_orchestrator
from src.agents.agentic_brain import SimpleSafetyInput

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_medical_emergency():
    """Example: Medical emergency requiring immediate response."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Medical Emergency - HIGH Priority")
    print("="*60)

    safety_input = {
        "video_id": "20251025_161628_d5957a56_video_68fd3c9a73bc8198b786a1d8e7b8874309f1b0907b4a562b",
        "safety_status": "HIGH",
        "scene_description": "A worker in a warehouse, wearing a safety vest, is operating a pallet jack. He shows signs of distress, sweating heavily, and nearly collapses, prompting another worker to intervene.",
        "predictions": {
            "probability": 0.9,
            "incident_type": "Medical Emergency - First Aid/Ambulance"
        },
        "safety_response": "Immediately provide first aid, move the worker to a cooler area, and offer water. Monitor his condition closely. If symptoms persist or worsen, call emergency medical services. Investigate potential causes such as heat stress or overexertion and implement preventative measures."
    }

    response = await safety_orchestrator.process_safety_input(safety_input)

    print(f"Plan ID: {response.plan_id}")
    print(f"Overall Success: {response.overall_success}")
    print(f"Execution Time: {response.total_execution_time:.2f}s")
    print(f"Actions Executed: {len(response.execution_results)}")

    print("\nAction Plan:")
    for i, action in enumerate(response.action_plan.actions, 1):
        print(f"  {i}. {action.tool_name}")
        print(f"     Reasoning: {action.reasoning}")
        print(f"     Priority: {action.priority}")
        print(f"     Requires Approval: {action.requires_approval}")

    print("\nExecution Results:")
    for result in response.execution_results:
        status = "✅ SUCCESS" if result.success else "❌ FAILED"
        print(f"  {result.action.tool_name}: {status}")
        if result.error_message:
            print(f"    Error: {result.error_message}")
        if result.result:
            print(f"    Result: {json.dumps(result.result, indent=4)}")


async def example_fall_hazard():
    """Example: Fall hazard requiring immediate safety measures."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Fall Hazard - CRITICAL Priority")
    print("="*60)

    safety_input = {
        "video_id": "20251025_142315_a7b8c9d0_video_fall_hazard_detection",
        "safety_status": "CRITICAL",
        "scene_description": "Worker on scaffolding 20 feet high without safety harness, no guardrails visible, showing signs of unsteady movement near edge.",
        "predictions": {
            "probability": 0.95,
            "incident_type": "Fall from Height - Potential Fatal"
        },
        "safety_response": "IMMEDIATE ACTION REQUIRED: Stop all work at height. Deploy emergency response team. Secure area below. Install fall protection immediately. Worker must not move until safety measures in place."
    }

    response = await safety_orchestrator.process_safety_input(safety_input)

    print(f"Plan ID: {response.plan_id}")
    print(f"Overall Success: {response.overall_success}")
    print(f"Execution Time: {response.total_execution_time:.2f}s")

    print("\nCritical Actions Taken:")
    for result in response.execution_results:
        if result.action.priority in ['critical', 'high']:
            status = "✅ EXECUTED" if result.success else "❌ FAILED"
            print(f"  • {result.action.tool_name}: {status}")
            print(f"    {result.action.reasoning}")


async def example_ppe_violation():
    """Example: PPE violation requiring supervisor notification."""
    print("\n" + "="*60)
    print("EXAMPLE 3: PPE Violation - MEDIUM Priority")
    print("="*60)

    safety_input = {
        "video_id": "20251025_093045_b2c3d4e5_video_ppe_violation",
        "safety_status": "MEDIUM",
        "scene_description": "Three workers in construction area, two wearing hard hats but one worker without head protection while operating power tools.",
        "predictions": {
            "probability": 0.6,
            "incident_type": "PPE Violation - Head Protection"
        },
        "safety_response": "Worker without hard hat should immediately stop work and obtain proper head protection. Supervisor notification required. Brief safety reminder for all workers."
    }

    response = await safety_orchestrator.process_safety_input(safety_input)

    print(f"Plan ID: {response.plan_id}")
    print(f"Actions: {len(response.action_plan.actions)}")

    print("\nNotification Actions:")
    for result in response.execution_results:
        if 'notify' in result.action.tool_name or 'sms' in result.action.tool_name:
            print(f"  • {result.action.tool_name}")
            if result.result:
                print(f"    Recipients: {result.action.parameters.get('recipients', [])}")
                print(f"    Message: {result.action.parameters.get('message', '')[:100]}...")


async def example_safe_conditions():
    """Example: Safe working conditions with standard logging."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Safe Conditions - LOW Priority")
    print("="*60)

    safety_input = {
        "video_id": "20251025_140022_f6g7h8i9_video_safe_operations",
        "safety_status": "LOW",
        "scene_description": "Workers properly equipped with full PPE, following safety procedures, good housekeeping, no immediate hazards visible.",
        "predictions": {
            "probability": 0.1,
            "incident_type": "No significant risk identified"
        },
        "safety_response": "Continue current safety practices. All workers demonstrating good safety compliance. Regular monitoring recommended."
    }

    response = await safety_orchestrator.process_safety_input(safety_input)

    print(f"Plan ID: {response.plan_id}")
    print(f"Actions: {len(response.action_plan.actions)}")
    print("Safe conditions - standard logging and monitoring procedures applied.")


async def batch_processing_example():
    """Example: Processing multiple safety inputs in batch."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Batch Processing Multiple Videos")
    print("="*60)

    safety_inputs = [
        {
            "video_id": "batch_001",
            "safety_status": "MEDIUM",
            "scene_description": "Worker not wearing safety glasses while grinding",
            "predictions": {"probability": 0.7, "incident_type": "Eye injury risk"},
            "safety_response": "Stop work, provide safety glasses, brief safety reminder"
        },
        {
            "video_id": "batch_002",
            "safety_status": "HIGH",
            "scene_description": "Electrical work without lockout/tagout procedure",
            "predictions": {"probability": 0.85, "incident_type": "Electrical shock hazard"},
            "safety_response": "Immediate work stoppage, implement LOTO, electrical safety inspection"
        },
        {
            "video_id": "batch_003",
            "safety_status": "LOW",
            "scene_description": "Proper lifting technique, good PPE compliance",
            "predictions": {"probability": 0.2, "incident_type": "Minor strain risk"},
            "safety_response": "Continue current practices, monitor for fatigue"
        }
    ]

    responses = await safety_orchestrator.batch_process(safety_inputs)

    print(f"Processed {len(responses)} videos")
    for response in responses:
        print(f"  • {response.video_id}: {response.safety_input.safety_status} -> {response.overall_success}")


async def demonstrate_approval_workflow():
    """Example: Action requiring approval workflow."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Approval Workflow - High-Risk Action")
    print("="*60)

    safety_input = {
        "video_id": "approval_demo_001",
        "safety_status": "CRITICAL",
        "scene_description": "Structural instability detected, immediate evacuation recommended",
        "predictions": {"probability": 0.92, "incident_type": "Structural collapse risk"},
        "safety_response": "EVACUATE IMMEDIATELY - structural integrity compromised"
    }

    response = await safety_orchestrator.process_safety_input(safety_input)

    print("Approval Workflow Results:")
    for result in response.execution_results:
        if result.requires_approval:
            print(f"  • {result.action.tool_name}: {result.approval_status}")


async def main():
    """Run all examples."""
    print("🏗️  Construction Safety Agent System - Example Usage")
    print("=" * 80)

    # Initialize the agent system
    print("Initializing Safety Agent System...")
    await safety_orchestrator.initialize()
    print("✅ System initialized successfully!")

    try:
        # Run examples
        await example_medical_emergency()
        await example_fall_hazard()
        await example_ppe_violation()
        await example_safe_conditions()
        await batch_processing_example()
        await demonstrate_approval_workflow()

        # Show system statistics
        print("\n" + "="*60)
        print("SYSTEM STATISTICS")
        print("="*60)
        stats = safety_orchestrator.get_stats()
        print(f"Total Responses: {stats['total_responses']}")
        print(f"Success Rate: {stats['success_rate']:.1%}")
        print(f"Average Response Time: {stats['avg_response_time']:.2f}s")
        print(f"Actions Executed: {stats['actions_executed']}")
        print(f"Actions Requiring Approval: {stats['actions_requiring_approval']}")

    except Exception as e:
        logger.error(f"Example execution failed: {str(e)}")
        raise

    print("\n🎉 All examples completed successfully!")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())