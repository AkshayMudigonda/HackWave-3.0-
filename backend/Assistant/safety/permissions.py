"""
Permission checks: evaluates whether a given tool call is permitted
under the active policy.
"""
from core.models import ToolRequest
from safety.policy import SafetyPolicy


class PermissionManager:
    """Checks permissions against policy before tool execution."""

    def __init__(self, policy: SafetyPolicy = None):
        self.policy = policy or SafetyPolicy()

    def check_permission(self, request: ToolRequest) -> bool:
        return self.policy.is_tool_allowed(request.tool)
