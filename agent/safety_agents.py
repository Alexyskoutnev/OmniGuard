import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.src.agent import Agent
from agent.src.runner import Runner
from agent.tools.compliance_tools import detect_compliance_violation
from agent.tools.ems_tools import detect_ems_hazard
from agent.tools.fire_tools import detect_fire_hazard
from agent.tools.notification_tools import send_site_alert

ems_agent = Agent(
    name="EMS Safety Agent",
    instructions=(
        "You are an emergency medical services safety specialist. You detect and respond to medical emergencies "
        "on construction sites including chest pain, heat stroke, severe lacerations, allergic reactions, "
        "and diabetic emergencies. Provide immediate action steps and determine if 911 should be called. "
        "Be specific about symptoms observed and urgency level."
    ),
    tools=[detect_ems_hazard, send_site_alert],
    handoff_description="Use for medical emergencies, worker health issues, injuries requiring immediate medical attention",
)

fire_agent = Agent(
    name="Fire Safety Agent",
    instructions=(
        "You are a fire safety specialist. You identify fire hazards including spontaneous combustion risks, "
        "welding sparks near combustibles, electrical overloads, fuel storage violations, and battery thermal "
        "runaway. Provide fire prevention steps and emergency response procedures. Be specific about ignition "
        "sources and combustible materials present."
    ),
    tools=[detect_fire_hazard, send_site_alert],
    handoff_description="Use for fire hazards, welding operations, electrical issues, combustible material storage",
)

compliance_agent = Agent(
    name="PPE Compliance Agent",
    instructions=(
        "You are a PPE compliance specialist. You identify workers not wearing required personal protective "
        "equipment including hard hats, high-visibility clothing, fall protection harnesses, hearing "
        "protection, and respirators. Enforce PPE requirements and stop work if violations create imminent danger. "
        "Be specific about what PPE is missing and why it's required."
    ),
    tools=[detect_compliance_violation, send_site_alert],
    handoff_description="Use for PPE violations, safety equipment issues, compliance enforcement",
)

safety_router_agent = Agent(
    name="Safety Router Agent",
    instructions=(
        "You are the main safety coordinator. Analyze construction site scenarios and determine which "
        "type of hazard is present. Route to the appropriate specialist agent:\n"
        "- EMS Agent: Medical emergencies, worker health issues, heat-related illness\n"
        "- Fire Agent: Fire hazards, ignition sources, combustibles\n"
        "- PPE Compliance Agent: Missing or improper safety equipment\n\n"
        "If multiple hazards exist, prioritize: EMS = Fire > Compliance"
    ),
    handoffs=[ems_agent, fire_agent, compliance_agent],
)


def create_runner(api_key: str = "", verbose: bool = True) -> Runner:
    return Runner(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key, verbose=verbose)


def run_agent_system(input: str, runner: Runner, max_handoffs: int = 5) -> str:
    result = runner.run_with_handoffs(
        safety_router_agent,
        f"Analyze this construction site scenario for safety hazards:\n\n{input}",
        max_handoffs=max_handoffs,
    )
    return result.output
