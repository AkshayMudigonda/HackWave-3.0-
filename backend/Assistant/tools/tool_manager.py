"""
Tool manager: resolves tool names to implementations, validates inputs,
and executes tool calls on behalf of the agent.
"""


from typing import Dict, Any

from core.models import ToolRequest, ToolResult
from core.results import success_result, failure_result
from core.exceptions import ToolNotFoundError


class ToolManager:

    def __init__(self):

        self.tools: Dict[str, Any] = {}

    def register(self, name: str, tool: Any):

        if not name:
            raise ValueError("Tool name cannot be empty.")

        self.tools[name.lower()] = tool

    def unregister(self, name: str):

        self.tools.pop(name.lower(), None)

    def has_tool(self, name: str) -> bool:

        return name.lower() in self.tools

    def get_tool(self, name: str):

        tool = self.tools.get(name.lower())

        if tool is None:
            raise ToolNotFoundError(
                f"Tool not found: {name}"
            )

        return tool

    def list_tools(self):

        return list(self.tools.keys())

    def execute(self, request: ToolRequest) -> ToolResult:

        try:

            tool = self.get_tool(request.tool)

        except ToolNotFoundError as exc:

            return failure_result(
                message=str(exc),
                error=str(exc),
            )

        try:

            if hasattr(tool, "execute"):

                result = tool.execute(request)

            elif hasattr(tool, "run"):

                result = tool.run(
                    request.action,
                    request.parameters,
                )

            else:

                return failure_result(
                    message=f"Tool '{request.tool}' has no execute method.",
                    error="Invalid tool interface.",
                )

            if isinstance(result, ToolResult):
                return result

            if isinstance(result, dict):

                return ToolResult(
                    success=result.get(
                        "success",
                        True,
                    ),
                    data=result.get("data"),
                    message=result.get(
                        "message",
                        "",
                    ),
                    error=result.get(
                        "error"
                    ),
                )

            return success_result(
                data=result
            )

        except Exception as exc:

            return failure_result(
                message=f"Tool '{request.tool}' failed.",
                error=str(exc),
            )