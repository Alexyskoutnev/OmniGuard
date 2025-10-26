class AgentError(Exception):
    """Base exception for agent-related errors"""

    pass


class ToolError(AgentError):
    """Exception raised when tool execution fails"""

    pass


class HandoffError(AgentError):
    """Exception raised when handoff to another agent fails"""

    pass


class ContextError(AgentError):
    """Exception raised for context-related errors"""

    pass


class ValidationError(AgentError):
    """Exception raised when input/output validation fails"""

    pass
