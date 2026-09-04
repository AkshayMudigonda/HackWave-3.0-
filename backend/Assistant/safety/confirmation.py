"""
Handles user confirmation flows for actions flagged as needing
explicit approval before execution.
"""
from typing import Callable, Optional
from core.models import ToolRequest
from safety.policy import SafetyPolicy


class ConfirmationHandler:
    """Prompts for and verifies user confirmation for sensitive tool actions."""

    def __init__(self, policy: SafetyPolicy = None, prompt_fn: Optional[Callable[[str], bool]] = None):
        self.policy = policy or SafetyPolicy()
        self.prompt_fn = prompt_fn

    def requires_confirmation(self, request: ToolRequest) -> bool:
        return self.policy.needs_confirmation(request.tool, request.action)

    def request_confirmation(self, request: ToolRequest) -> bool:
        if not self.requires_confirmation(request):
            return True
        if self.prompt_fn:
            return self.prompt_fn(f"Are you sure you want to execute {request.tool}:{request.action}?")
        # Absence of an interactive callback must never silently approve risk.
        return False
