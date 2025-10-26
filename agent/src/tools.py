import inspect
import json
from collections.abc import Callable
from typing import Any, get_type_hints

from .exceptions import ToolError


class Tool:
    """
    Represents a tool that can be used by an agent
    """

    def __init__(
        self, name: str, function: Callable, description: str, parameters_schema: dict[str, Any]
    ):
        """
        Initialize a tool

        Args:
            name: Tool name
            function: Python function to execute
            description: Tool description
            parameters_schema: JSON schema for parameters
        """
        self.name = name
        self.function = function
        self.description = description
        self.parameters_schema = parameters_schema

    def to_openai_format(self) -> dict[str, Any]:
        """
        Convert tool to OpenAI function calling format

        Returns:
            Tool definition in OpenAI format
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters_schema,
            },
        }

    def execute(self, arguments: dict[str, Any]) -> Any:
        """
        Execute the tool with given arguments

        Args:
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ToolError: If tool execution fails
        """
        try:
            return self.function(**arguments)
        except Exception as e:
            raise ToolError(f"Error executing tool '{self.name}': {e!s}") from e

    def __repr__(self):
        return f"Tool(name='{self.name}')"


def tool(description: str | None = None):
    """
    Decorator to convert a Python function into a tool

    Usage:
        @tool(description="Calculate the sum of two numbers")
        def add(a: int, b: int) -> int:
            return a + b

    Args:
        description: Tool description (uses docstring if not provided)

    Returns:
        Decorated function with tool metadata
    """

    def decorator(func: Callable) -> Tool:
        # Get function metadata
        func_name = func.__name__
        func_description = description or func.__doc__ or f"Execute {func_name}"

        # Get type hints
        type_hints = get_type_hints(func)
        sig = inspect.signature(func)

        # Build parameters schema
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            # Skip self and cls parameters
            if param_name in ("self", "cls"):
                continue

            param_type = type_hints.get(param_name, Any)

            # Convert Python types to JSON schema types
            json_type = _python_type_to_json_type(param_type)

            properties[param_name] = {"type": json_type, "description": f"Parameter {param_name}"}

            # Check if parameter is required (no default value)
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        parameters_schema = {"type": "object", "properties": properties, "required": required}

        # Create and return Tool instance
        return Tool(
            name=func_name,
            function=func,
            description=func_description,
            parameters_schema=parameters_schema,
        )

    return decorator


def _python_type_to_json_type(python_type: type) -> str:
    """
    Convert Python type to JSON schema type

    Args:
        python_type: Python type

    Returns:
        JSON schema type string
    """
    type_mapping = {
        int: "integer",
        float: "number",
        str: "string",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    # Handle Optional types
    if hasattr(python_type, "__origin__"):
        if python_type.__origin__ is list:
            return "array"
        elif python_type.__origin__ is dict:
            return "object"

    return type_mapping.get(python_type, "string")


def execute_tool_call(tool: Tool, tool_call) -> str:
    """
    Execute a tool call and return the result as a string

    Args:
        tool: Tool to execute
        tool_call: Tool call object from model response

    Returns:
        String representation of the result
    """
    try:
        # Parse arguments
        if isinstance(tool_call.function.arguments, str):
            arguments = json.loads(tool_call.function.arguments)
        else:
            arguments = tool_call.function.arguments

        # Execute tool
        result = tool.execute(arguments)

        # Convert result to string
        if isinstance(result, dict | list):
            return json.dumps(result)
        else:
            return str(result)

    except Exception as e:
        return f"Error: {e!s}"
