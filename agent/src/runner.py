import json
import os
import time

from openai import OpenAI

from .agent import Agent
from .context import Context
from .exceptions import AgentError, HandoffError
from .logger import AgentLogger
from .tools import execute_tool_call
from .types import AgentResult


class Runner:
    """
    Executes agents and manages the agent loop
    """

    def __init__(
        self,
        client: OpenAI | None = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        api_key: str = "",
        verbose: bool = True,
    ):
        """
        Initialize the runner

        Args:
            client: OpenAI client (creates one if not provided)
            base_url: API base URL
            api_key: API key (defaults to NVIDIA_API_KEY env var)
            verbose: Enable verbose logging
        """
        if client is None:
            if not api_key:
                api_key = os.getenv(
                    "NVIDIA_API_KEY",
                    "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",
                )
            self.client = OpenAI(base_url=base_url, api_key=api_key)
        else:
            self.client = client

        self.max_iterations = 10  # Prevent infinite loops
        self.logger = AgentLogger(verbose=verbose)

    def run(self, agent: Agent, user_input: str, context: Context | None = None) -> AgentResult:
        """
        Run an agent with user input

        Args:
            agent: Agent to run
            user_input: User message
            context: Conversation context (creates new if not provided)

        Returns:
            AgentResult with final output

        Raises:
            AgentError: If agent execution fails
        """
        # Start logging
        self.logger.start_agent(agent.name)

        # Create or clone context
        context = Context() if context is None else context.clone()

        # Add system message with instructions
        if not context.messages or context.messages[0].role != "system":
            context.add_system_message(agent.instructions)

        # Add user input
        context.add_user_message(user_input)

        # Run agent loop
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            self.logger.log_iteration(iteration)

            # Call the model
            response = self._call_model(agent, context)

            # Check if response has tool calls
            tool_calls = response.tool_calls

            if tool_calls:
                # Add assistant message with tool calls
                context.add_assistant_message(
                    content=response.content or "",
                    tool_calls=[
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in tool_calls
                    ],
                )

                # Execute tools
                handoff_detected = False
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name

                    # Check if this is a handoff tool
                    if tool_name.startswith("handoff_to_"):
                        handoff_detected = True
                        target_agent_name = (
                            tool_name.replace("handoff_to_", "").replace("_", " ").title()
                        )
                        target_agent = agent.get_handoff_agent(target_agent_name)

                        if target_agent:
                            # Log handoff
                            self.logger.log_handoff_attempt(agent.name, target_agent_name)
                            self.logger.end_agent(
                                f"Handing off to {target_agent_name}", handoff_to=target_agent_name
                            )

                            # Return result indicating handoff
                            return AgentResult(
                                output=f"Handing off to {target_agent_name}",
                                agent_name=agent.name,
                                messages=context.messages,
                                handoff_to=target_agent_name,
                            )
                        else:
                            raise HandoffError(f"Handoff agent '{target_agent_name}' not found")

                    # Regular tool execution
                    tool = agent.get_tool(tool_name)
                    if tool:
                        # Parse arguments
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                        except json.JSONDecodeError:
                            arguments = {}

                        # Execute tool with timing
                        start_time = time.time()
                        result = execute_tool_call(tool, tool_call)
                        duration_ms = (time.time() - start_time) * 1000

                        # Log tool call
                        self.logger.log_tool_call(
                            tool_name=tool_name,
                            arguments=arguments,
                            result=result,
                            duration_ms=duration_ms,
                            success=not result.startswith("Error"),
                        )

                        context.add_tool_message(
                            tool_call_id=tool_call.id, name=tool_name, content=result
                        )
                    else:
                        # Tool not found
                        error_msg = f"Error: Tool '{tool_name}' not found"
                        self.logger.log_tool_call(
                            tool_name=tool_name,
                            arguments={},
                            result=error_msg,
                            duration_ms=0,
                            success=False,
                            error=error_msg,
                        )
                        context.add_tool_message(
                            tool_call_id=tool_call.id, name=tool_name, content=error_msg
                        )

                if handoff_detected:
                    # Already returned above
                    pass

                # Continue loop to get next response
                continue

            else:
                # No tool calls - this is the final response
                output = response.content or ""
                context.add_assistant_message(output)

                # Log completion
                self.logger.end_agent(output)

                return AgentResult(output=output, agent_name=agent.name, messages=context.messages)

        # Max iterations reached
        self.logger.end_agent("Max iterations exceeded")
        raise AgentError(
            f"Agent '{agent.name}' exceeded maximum iterations ({self.max_iterations})"
        )

    def run_with_handoffs(
        self, agent: Agent, user_input: str, context: Context | None = None, max_handoffs: int = 5
    ) -> AgentResult:
        """
        Run an agent with automatic handoff support

        Args:
            agent: Initial agent to run
            user_input: User message
            context: Conversation context
            max_handoffs: Maximum number of handoffs allowed

        Returns:
            AgentResult with final output
        """
        current_agent = agent
        handoff_count = 0

        while handoff_count < max_handoffs:
            # Prepare tools including handoff tools
            tools_with_handoffs = current_agent.tools.copy()

            # Add handoff tools for each available handoff agent
            for handoff_agent in current_agent.handoffs:
                handoff_tool = handoff_agent.create_handoff_tool()
                if handoff_tool:
                    tools_with_handoffs.append(handoff_tool)

            # Temporarily set tools
            original_tools = current_agent.tools
            current_agent.tools = tools_with_handoffs
            current_agent._tool_map = {tool.name: tool for tool in tools_with_handoffs}

            # Run agent
            result = self.run(current_agent, user_input, context)

            # Restore original tools
            current_agent.tools = original_tools
            current_agent._tool_map = {tool.name: tool for tool in original_tools}

            # Check if handoff occurred
            if result.handoff_to:
                handoff_count += 1
                # Find the handoff agent
                next_agent = current_agent.get_handoff_agent(result.handoff_to)
                if next_agent:
                    current_agent = next_agent
                    context = Context(result.messages)
                    user_input = f"[Continuing from {result.agent_name}]"
                else:
                    # Handoff agent not found, return result
                    return result
            else:
                # No handoff, return final result
                return result

        # Max handoffs reached
        raise AgentError(f"Maximum handoffs ({max_handoffs}) exceeded")

    def _call_model(self, agent: Agent, context: Context):
        """
        Call the model API

        Args:
            agent: Agent to use
            context: Current context

        Returns:
            Model response
        """
        messages = context.get_messages_as_dict()

        # Log model call
        self.logger.log_model_call(agent.model, len(messages))

        # Build API call parameters
        api_params = {
            "model": agent.model,
            "messages": messages,
            "temperature": agent.temperature,
            "max_tokens": agent.max_tokens,
        }

        # Add tools if agent has them
        if agent.has_tools():
            api_params["tools"] = agent.get_tools_for_api()
            api_params["tool_choice"] = "auto"

        # Call API
        response = self.client.chat.completions.create(**api_params)

        return response.choices[0].message

    def get_summary(self) -> str:
        """
        Get execution summary from logger

        Returns:
            Formatted summary string
        """
        return self.logger.get_summary()
