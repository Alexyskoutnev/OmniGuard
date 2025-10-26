from typing import Any, Optional

from .tools import Tool


class Agent:
    """
    An AI agent with instructions, tools, and handoff capabilities
    """

    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "nvidia/nvidia-nemotron-nano-9b-v2",
        tools: list[Tool] | None = None,
        handoffs: list["Agent"] | None = None,
        handoff_description: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ):
        """
        Initialize an agent

        Args:
            name: Agent name
            instructions: System instructions for the agent
            model: Model to use (default: NVIDIA Nemotron)
            tools: List of tools available to the agent
            handoffs: List of agents this agent can hand off to
            handoff_description: Description for when to hand off to this agent
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []
        self.handoffs = handoffs or []
        self.handoff_description = handoff_description
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Create tool map for quick lookup
        self._tool_map: dict[str, Tool] = {tool.name: tool for tool in self.tools}

    def get_tool(self, name: str) -> Tool | None:
        """
        Get a tool by name

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tool_map.get(name)

    def get_tools_for_api(self) -> list[dict[str, Any]]:
        """
        Get tools in OpenAI API format

        Returns:
            List of tool definitions
        """
        return [tool.to_openai_format() for tool in self.tools]

    def has_tools(self) -> bool:
        """Check if agent has any tools"""
        return len(self.tools) > 0

    def has_handoffs(self) -> bool:
        """Check if agent can hand off to other agents"""
        return len(self.handoffs) > 0

    def get_handoff_agent(self, name: str) -> Optional["Agent"]:
        """
        Get a handoff agent by name (case-insensitive)

        Args:
            name: Agent name

        Returns:
            Agent instance or None if not found
        """
        name_lower = name.lower()
        for agent in self.handoffs:
            if agent.name.lower() == name_lower:
                return agent
        return None

    def create_handoff_tool(self) -> Tool | None:
        """
        Create a special tool for handing off to this agent

        Returns:
            Handoff tool or None if no handoff description
        """
        if not self.handoff_description:
            return None

        def handoff_func(reason: str = "") -> str:
            return f"Handing off to {self.name}: {reason}"

        from .tools import Tool

        return Tool(
            name=f"handoff_to_{self.name.lower().replace(' ', '_')}",
            function=handoff_func,
            description=self.handoff_description,
            parameters_schema={
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "Reason for the handoff"}
                },
                "required": [],
            },
        )

    def __repr__(self):
        return f"Agent(name='{self.name}', tools={len(self.tools)}, handoffs={len(self.handoffs)})"
