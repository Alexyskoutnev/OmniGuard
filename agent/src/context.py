from typing import Any

from .types import Message


class Context:
    """
    Manages conversation context and history across agent runs
    """

    def __init__(self, initial_messages: list[Message] | None = None):
        """
        Initialize context with optional message history

        Args:
            initial_messages: Initial conversation history
        """
        self.messages: list[Message] = initial_messages or []
        self.metadata: dict[str, Any] = {}

    def add_message(self, role: str, content: str | None = None, **kwargs):
        """
        Add a message to the conversation history

        Args:
            role: Message role (system, user, assistant, tool)
            content: Message content
            **kwargs: Additional message attributes
        """
        message = Message(role=role, content=content, **kwargs)
        self.messages.append(message)
        return message

    def add_user_message(self, content: str):
        """Add a user message"""
        return self.add_message("user", content)

    def add_assistant_message(self, content: str, **kwargs):
        """Add an assistant message"""
        return self.add_message("assistant", content, **kwargs)

    def add_system_message(self, content: str):
        """Add a system message"""
        return self.add_message("system", content)

    def add_tool_message(self, tool_call_id: str, name: str, content: str):
        """Add a tool result message"""
        return self.add_message("tool", content=content, name=name, tool_call_id=tool_call_id)

    def get_messages_as_dict(self) -> list[dict[str, Any]]:
        """
        Convert messages to dictionary format for API calls

        Returns:
            List of message dictionaries
        """
        result = []
        for msg in self.messages:
            msg_dict = {"role": msg.role}

            if msg.content:
                msg_dict["content"] = msg.content

            if msg.name:
                msg_dict["name"] = msg.name

            if msg.tool_calls:
                msg_dict["tool_calls"] = msg.tool_calls

            if msg.tool_call_id:
                msg_dict["tool_call_id"] = msg.tool_call_id

            result.append(msg_dict)

        return result

    def clear(self):
        """Clear all messages from context"""
        self.messages = []
        self.metadata = {}

    def clone(self) -> "Context":
        """Create a copy of this context"""
        new_context = Context()
        new_context.messages = self.messages.copy()
        new_context.metadata = self.metadata.copy()
        return new_context

    def __len__(self):
        return len(self.messages)

    def __repr__(self):
        return f"Context(messages={len(self.messages)})"
