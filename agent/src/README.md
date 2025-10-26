# Mini Agent Framework

A lightweight agent framework inspired by OpenAI's Agents SDK, designed to work with NVIDIA endpoints and tool calling.

## Features

- 🤖 **Simple Agent API** - Define agents with instructions and tools
- 🔧 **Tool Calling** - Automatic tool schema generation from Python functions
- 🔄 **Agent Handoffs** - Route between specialized agents
- 💬 **Context Management** - Automatic conversation history tracking
- 🚀 **NVIDIA Compatible** - Works with NVIDIA's hosted inference API

## Architecture

The framework follows the OpenAI Agents SDK philosophy:

- **Agent** - LLM with instructions and tools
- **Tools** - Python functions decorated with `@tool`
- **Runner** - Executes the agent loop with automatic tool calling
- **Context** - Manages conversation history
- **Handoffs** - Allows agents to delegate to specialists

## Installation

```bash
pip install openai pydantic
```

## Quick Start

### Basic Agent with Tools

```python
from agent import Agent, tool, Runner

# Define a tool
@tool(description="Add two numbers")
def add(a: int, b: int) -> int:
    return a + b

# Create an agent
agent = Agent(
    name="Math Assistant",
    instructions="You help with math problems",
    tools=[add]
)

# Create runner
runner = Runner(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="your-api-key"
)

# Run the agent
result = runner.run(agent, "What is 5 + 7?")
print(result.output)
```

### Multi-Agent with Handoffs

```python
from agent import Agent, Runner

# Create specialist agents
math_agent = Agent(
    name="Math Tutor",
    instructions="You help with math questions",
    handoff_description="Use for math questions"
)

history_agent = Agent(
    name="History Tutor",
    instructions="You help with history questions",
    handoff_description="Use for history questions"
)

# Create triage agent
triage = Agent(
    name="Triage",
    instructions="Route questions to the right specialist",
    handoffs=[math_agent, history_agent]
)

# Run with automatic handoffs
runner = Runner(base_url="...", api_key="...")
result = runner.run_with_handoffs(triage, "What is 10 + 5?")
```

## Core Components

### Agent

```python
Agent(
    name: str,                      # Agent name
    instructions: str,              # System instructions
    model: str,                     # Model to use (default: NVIDIA Nemotron)
    tools: List[Tool],              # Available tools
    handoffs: List[Agent],          # Agents to hand off to
    handoff_description: str,       # When to use this agent
    temperature: float,             # Sampling temperature
    max_tokens: int                 # Max response tokens
)
```

### Tool Decorator

```python
@tool(description="Tool description")
def my_tool(param1: int, param2: str) -> str:
    """Function docstring"""
    return f"Result: {param1}, {param2}"
```

- Automatically generates JSON schema from type hints
- Supports int, float, str, bool, list, dict types
- Uses docstring as description if not provided

### Runner

```python
runner = Runner(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="your-key"
)

# Run single agent
result = runner.run(agent, user_input)

# Run with handoffs
result = runner.run_with_handoffs(agent, user_input, max_handoffs=5)
```

### Context

```python
from agent import Context

# Create context
context = Context()

# Add messages
context.add_user_message("Hello")
context.add_assistant_message("Hi there!")
context.add_system_message("You are helpful")

# Use context across runs
result = runner.run(agent, "Continue", context=context)
```

## Examples

See the example files:

- `example_basic_agent.py` - Basic agent with tools
- `example_multi_agent.py` - Multi-agent with handoffs

Run examples:

```bash
python example_basic_agent.py
python example_multi_agent.py
```

## How It Works

### Agent Loop

1. **Initialize**: Add system instructions and user message to context
2. **Call Model**: Send messages to LLM with available tools
3. **Check Response**:
   - If tool calls → Execute tools, add results to context, repeat
   - If handoff → Switch to target agent
   - Otherwise → Return final response
4. **Iterate**: Continue until response or max iterations reached

### Tool Calling

1. Decorator converts Python function to Tool object
2. Tool generates OpenAI-compatible function schema
3. Runner includes tools in API call
4. Model returns tool calls in response
5. Runner executes tools and adds results to context
6. Loop continues until final response

### Handoffs

1. Each agent can define handoff targets
2. Handoff tools are automatically created
3. Model calls handoff tool when needed
4. Runner switches to target agent
5. Conversation continues with new agent

## API Reference

### Agent

- `get_tool(name)` - Get tool by name
- `get_tools_for_api()` - Get tools in OpenAI format
- `has_tools()` - Check if agent has tools
- `has_handoffs()` - Check if agent has handoffs
- `get_handoff_agent(name)` - Get handoff agent by name

### Runner

- `run(agent, input, context)` - Run agent once
- `run_with_handoffs(agent, input, context, max_handoffs)` - Run with automatic handoffs

### Context

- `add_message(role, content)` - Add message
- `add_user_message(content)` - Add user message
- `add_assistant_message(content)` - Add assistant message
- `add_system_message(content)` - Add system message
- `add_tool_message(id, name, content)` - Add tool result
- `get_messages_as_dict()` - Get messages for API
- `clear()` - Clear all messages
- `clone()` - Create a copy

### Tool

- `to_openai_format()` - Convert to OpenAI schema
- `execute(arguments)` - Execute tool function

## License

MIT
