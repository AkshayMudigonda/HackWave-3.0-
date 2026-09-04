"""
Defines safety policies: which actions are allowed, blocked, or require
confirmation.
"""
from dataclasses import dataclass, field
from typing import Set


@dataclass
class SafetyPolicy:
    """Configurable safety policy for tools and actions."""
    blocked_tools: Set[str] = field(default_factory=set)
    require_confirmation_tools: Set[str] = field(default_factory=lambda: {"terminal"})
    allowed_tools: Set[str] = field(default_factory=lambda: {
        "calculator", "datetime", "browser", "applications", "filesystem", "terminal"
    })

    def is_tool_allowed(self, tool_name: str) -> bool:
        name = tool_name.lower()
        if name in self.blocked_tools:
            return False
        return name in self.allowed_tools

    def needs_confirmation(self, tool_name: str, action: str = "") -> bool:
        return action.lower() in {"delete", "send_email", "book", "purchase"}
