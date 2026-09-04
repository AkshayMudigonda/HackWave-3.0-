"""Safety-gated action execution and immutable action history."""
import json
from core.models import ToolRequest, ToolResult
from database.database import Database
from safety.confirmation import ConfirmationHandler
from safety.permissions import PermissionManager
from safety.risk import RiskClassifier


class ActionExecutor:
    def __init__(self, tool_manager, database=None, permissions=None, confirmation=None):
        self.tool_manager = tool_manager
        self.database = database or Database()
        self.permissions = permissions or PermissionManager()
        self.confirmation = confirmation or ConfirmationHandler()
        self.risk = RiskClassifier()

    def execute(self, request: ToolRequest, task_id: str = "") -> ToolResult:
        level = self.risk.classify(request)
        if not self.permissions.check_permission(request):
            return self._record(task_id, request, level.value, ToolResult(False, message="Action is not permitted."))
        if level.value in {"HIGH", "CRITICAL"} or self.confirmation.requires_confirmation(request):
            if not self.confirmation.request_confirmation(request):
                return self._record(task_id, request, level.value, ToolResult(False, message="Waiting for explicit confirmation."))
        return self._record(task_id, request, level.value, self.tool_manager.execute(request))

    def _record(self, task_id, request, risk, result):
        self.database.execute("INSERT INTO actions (task_id, name, status, risk, parameters, result, error) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (task_id, f"{request.tool}:{request.action}", "COMPLETED" if result.success else "FAILED", risk,
             json.dumps(request.parameters, default=str), json.dumps(result.data, default=str), result.error))
        return result
