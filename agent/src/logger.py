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
        self._log_box(f"AGENT: {agent_name}", "START")

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
                self._log_box(f"HANDOFF -> {handoff_to}", "TRANSFER")
            else:
                self._log_box(f"COMPLETED ({duration_ms:.0f}ms)", "END")

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

        # Format arguments for display (shortened)
        args_display = []
        for k, v in arguments.items():
            v_str = str(v)
            if len(v_str) > 60:
                v_str = v_str[:57] + "..."
            args_display.append(f"{k}={v_str}")
        args_str = ", ".join(args_display)

        if success:
            self._log_tool(tool_name, args_str, result, duration_ms)
        else:
            self._log_error(f"Tool {tool_name} failed: {error}")

    def log_iteration(self, iteration: int):
        """
        Log an agent loop iteration

        Args:
            iteration: Iteration number
        """
        if self.current_trace:
            self.current_trace.iterations = iteration

        self._log_simple(f"├─ Iteration {iteration}")

    def log_model_call(self, model: str, message_count: int):
        """
        Log a model API call

        Args:
            model: Model name
            message_count: Number of messages in context
        """
        model_short = model.split("/")[-1] if "/" in model else model
        self._log_simple(f"│  ├─ Model: {model_short} ({message_count} msgs)")

    def log_handoff_attempt(self, from_agent: str, to_agent: str, reason: str = ""):
        """
        Log a handoff attempt

        Args:
            from_agent: Source agent name
            to_agent: Target agent name
            reason: Reason for handoff
        """
        self._log_simple(f"│  └─ Handoff: {from_agent} -> {to_agent}")

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

    def _log_box(self, message: str, box_type: str = "INFO"):
        """Log with box formatting"""
        if not self.verbose:
            return

        if box_type == "START":
            print(f"\n┌─ {message}")
        elif box_type == "END" or box_type == "TRANSFER":
            print(f"└─ {message}\n")

    def _log_simple(self, message: str):
        """Log simple line"""
        if self.verbose:
            print(message)

    def _log_tool(self, tool_name: str, args: str, result: str, duration_ms: float):
        """Log tool call with clean formatting"""
        if not self.verbose:
            return

        result_preview = result[:80].replace("\n", " ") if result else ""
        if len(result) > 80:
            result_preview += "..."

        print(f"│  ├─ Tool: {tool_name}")
        print(f"│  │  ├─ Args: {args}")
        print(f"│  │  ├─ Result: {result_preview}")
        print(f"│  │  └─ Time: {duration_ms:.1f}ms")

    def _log_error(self, message: str):
        """Log error message"""
        if self.verbose:
            print(f"│  └─ ERROR: {message}")

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
