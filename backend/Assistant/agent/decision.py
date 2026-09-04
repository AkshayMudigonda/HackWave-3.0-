"""
Decision module: selects the next action given the current plan,
context, and available tools, and formats single and multi-task responses.
"""
from typing import Any, List, Union
from core.models import AgentObservation, ToolResult


class Decision:

    def should_continue(
        self,
        result: Any,
    ) -> bool:
        if result is None:
            return False
        return False

    def format_response(
        self,
        result_or_results: Union[AgentObservation, ToolResult, List[Union[AgentObservation, ToolResult]], None],
    ) -> str:
        """Format single or multitasking observations into clear, human-readable text."""
        if result_or_results is None:
            return "I couldn't understand that request."

        # Handle list of observations (Multitasking result)
        if isinstance(result_or_results, list):
            if not result_or_results:
                return "No tasks were executed."

            if len(result_or_results) == 1:
                return self._format_single(result_or_results[0])

            lines = []
            for idx, item in enumerate(result_or_results, start=1):
                msg = self._format_single(item)
                lines.append(f"{idx}. {msg}")
            return "\n".join(lines)

        return self._format_single(result_or_results)

    def _format_single(
        self,
        result: Union[AgentObservation, ToolResult],
    ) -> str:
        if result is None:
            return "Task could not be completed."

        if result.success:
            if result.message:
                return result.message
            if result.data is not None:
                return str(result.data)
            return "Done."

        if result.message:
            return result.message

        if result.error:
            return f"Operation failed: {result.error}"

        return "The operation failed."