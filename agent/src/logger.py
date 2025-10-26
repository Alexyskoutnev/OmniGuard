from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ToolCallTrace:
    """Trace information for a tool call"""

    tool_name: str
    arguments: dict[str, Any]
    result: str
    duration_ms: float
    timestamp: str
    success: bool = True
    error: str | None = None


@dataclass
class AgentTrace:
    """Trace information for an agent execution"""

    agent_name: str
    start_time: str
    end_time: str | None = None
    duration_ms: float | None = None
    tool_calls: list[ToolCallTrace] = field(default_factory=list)
    iterations: int = 0
    handoff_to: str | None = None
    final_output: str | None = None


class AgentLogger:
    """
    Logger for tracking agent execution, tool calls, and handoffs
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the logger

        Args:
            verbose: Whether to print logs to console
        """
        self.verbose = verbose
        self.traces: list[AgentTrace] = []
        self.current_trace: AgentTrace | None = None
        self._indent_level = 0

    def start_agent(self, agent_name: str):
        """
        Start tracking an agent execution

        Args:
            agent_name: Name of the agent
        """
        self.current_trace = AgentTrace(
            agent_name=agent_name,
            start_time=datetime.now().isoformat(),
        )
        self._log(f"🤖 Starting agent: {agent_name}", "AGENT")

    def end_agent(self, output: str, handoff_to: str | None = None):
        """
        End tracking an agent execution

        Args:
            output: Final output from the agent
            handoff_to: Name of agent to hand off to (if any)
        """
        if self.current_trace:
            end_time = datetime.now()
            start_time = datetime.fromisoformat(self.current_trace.start_time)
            duration_ms = (end_time - start_time).total_seconds() * 1000

            self.current_trace.end_time = end_time.isoformat()
            self.current_trace.duration_ms = duration_ms
            self.current_trace.final_output = output
            self.current_trace.handoff_to = handoff_to

            if handoff_to:
                self._log(f"🔄 Handing off to: {handoff_to}", "HANDOFF")
            else:
                self._log(f"✅ Agent completed in {duration_ms:.2f}ms", "AGENT")

            self.traces.append(self.current_trace)
            self.current_trace = None

    def log_tool_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: str,
        duration_ms: float,
        success: bool = True,
        error: str | None = None,
    ):
        """
        Log a tool call

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            result: Tool result
            duration_ms: Execution duration in milliseconds
            success: Whether the tool call succeeded
            error: Error message if failed
        """
        trace = ToolCallTrace(
            tool_name=tool_name,
            arguments=arguments,
            result=result,
            duration_ms=duration_ms,
            timestamp=datetime.now().isoformat(),
            success=success,
            error=error,
        )

        if self.current_trace:
            self.current_trace.tool_calls.append(trace)

        # Format arguments for display
        args_str = ", ".join(f"{k}={v}" for k, v in arguments.items())

        if success:
            self._log(f"🔧 Tool call: {tool_name}({args_str})", "TOOL")
            self._log(f"   Result: {result[:100]}{'...' if len(result) > 100 else ''}", "TOOL")
            self._log(f"   Duration: {duration_ms:.2f}ms", "TOOL")
        else:
            self._log(f"❌ Tool call failed: {tool_name}({args_str})", "ERROR")
            self._log(f"   Error: {error}", "ERROR")

    def log_iteration(self, iteration: int):
        """
        Log an agent loop iteration

        Args:
            iteration: Iteration number
        """
        if self.current_trace:
            self.current_trace.iterations = iteration

        self._log(f"🔄 Iteration {iteration}", "LOOP")

    def log_model_call(self, model: str, message_count: int):
        """
        Log a model API call

        Args:
            model: Model name
            message_count: Number of messages in context
        """
        self._log(f"💬 Calling model: {model} (messages: {message_count})", "MODEL")

    def log_handoff_attempt(self, from_agent: str, to_agent: str, reason: str = ""):
        """
        Log a handoff attempt

        Args:
            from_agent: Source agent name
            to_agent: Target agent name
            reason: Reason for handoff
        """
        msg = f"🔀 Handoff: {from_agent} → {to_agent}"
        if reason:
            msg += f" (Reason: {reason})"
        self._log(msg, "HANDOFF")

    def get_summary(self) -> str:
        """
        Get a summary of all traces

        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("EXECUTION SUMMARY")
        lines.append("=" * 80)

        for i, trace in enumerate(self.traces, 1):
            lines.append(f"\nAgent {i}: {trace.agent_name}")
            lines.append(f"  Duration: {trace.duration_ms:.2f}ms")
            lines.append(f"  Iterations: {trace.iterations}")
            lines.append(f"  Tool Calls: {len(trace.tool_calls)}")

            if trace.tool_calls:
                lines.append("  Tools Used:")
                for tc in trace.tool_calls:
                    status = "✓" if tc.success else "✗"
                    lines.append(f"    {status} {tc.tool_name} ({tc.duration_ms:.2f}ms)")

            if trace.handoff_to:
                lines.append(f"  Handoff: → {trace.handoff_to}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def _log(self, message: str, level: str = "INFO"):
        """
        Internal logging method

        Args:
            message: Message to log
            level: Log level
        """
        if self.verbose:
            indent = "  " * self._indent_level
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] {indent}{message}")

    def indent(self):
        """Increase indentation level"""
        self._indent_level += 1

    def dedent(self):
        """Decrease indentation level"""
        self._indent_level = max(0, self._indent_level - 1)

    def clear(self):
        """Clear all traces"""
        self.traces = []
        self.current_trace = None
        self._indent_level = 0
