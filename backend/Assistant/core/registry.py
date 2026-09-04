"""
Registry: central lookup of available tools/handlers, populated at
startup by each tool package.
"""
from typing import Any, Dict, Optional
from core.exceptions import ToolNotFoundError


class ToolRegistry:
    """Registry mapping tool names to tool instances."""

    def __init__(self):
        self._tools: Dict[str, Any] = {}

    def register(self, name: str, tool: Any):
        if not name:
            raise ValueError("Tool name cannot be empty.")
        self._tools[name.lower()] = tool

    def unregister(self, name: str):
        self._tools.pop(name.lower(), None)

    def get(self, name: str) -> Any:
        tool = self._tools.get(name.lower())
        if tool is None:
            raise ToolNotFoundError(f"Tool not found: {name}")
        return tool

    def list_tools(self):
        return list(self._tools.keys())

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._tools
