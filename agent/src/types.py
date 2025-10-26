from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    """Represents a message in the conversation"""

    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str | None = None
    name: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None


@dataclass
class ToolCall:
    """Represents a tool call made by the agent"""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    """Represents the result of a tool execution"""

    tool_call_id: str
    name: str
    content: str
    success: bool = True
    error: str | None = None


class AgentResult:
    """Represents the final result from an agent execution"""

    def __init__(
        self,
        output: str,
        agent_name: str,
        messages: list[Message],
        tool_calls: list[ToolCall] | None = None,
        handoff_to: str | None = None,
    ):
        self.output = output
        self.agent_name = agent_name
        self.messages = messages
        self.tool_calls = tool_calls or []
        self.handoff_to = handoff_to

    def __str__(self):
        return self.output


ToolFunction = Callable[..., Any]
