"""
Applications tool: launches and controls desktop applications.
"""
from core.results import success, failure
from tools.applications.parser import ApplicationParser
from tools.applications.registry import ApplicationRegistry
from tools.applications.process_manager import ProcessManager


class ApplicationsTool:

    def __init__(self):
        self.parser = ApplicationParser()
        self.registry = ApplicationRegistry()
        self.process_manager = ProcessManager()

    def execute(self, request):

        raw_cmd = (
            getattr(request, "original_input", None)
            or (request.parameters.get("command") if isinstance(request.parameters, dict) else None)
            or ""
        )

        parsed = self.parser.parse(raw_cmd) if raw_cmd else None

        if not parsed:
            if request.action in ("open", "close", "restart") and isinstance(request.parameters, dict):
                app_param = request.parameters.get("application") or request.parameters.get("name")
                if app_param:
                    parsed = {
                        "action": request.action,
                        "application": app_param,
                    }

        if not parsed:
            return failure(
                "Invalid application command.",
                tool="applications",
            )

        application_name = parsed["application"]

        application = self.registry.find(
            application_name
        )

        if not application:
            return failure(
                f"Application not found: {application_name}",
                tool="applications",
                action=parsed["action"],
            )

        action = parsed["action"]

        if action == "open":
            result = self.process_manager.open(
                application
            )

            message = (
                f"Opening {application['name']}."
                if result
                else f"Unable to open {application['name']}."
            )
            if result and parsed.get("text"):
                message += " Text entry was not performed: interactive desktop automation is not configured."

        elif action == "close":
            result = self.process_manager.close(
                application
            )

            message = (
                f"Closing {application['name']}."
                if result
                else f"Unable to close {application['name']}."
            )

        elif action == "restart":
            result = self.process_manager.restart(
                application
            )

            message = (
                f"Restarting {application['name']}."
                if result
                else f"Unable to restart {application['name']}."
            )

        else:
            return failure(
                f"Unsupported action: {action}",
                tool="applications",
                action=action,
            )

        if result:
            return success(
                message,
                data=application,
                tool="applications",
                action=action,
            )

        return failure(
            message,
            data=application,
            tool="applications",
            action=action,
        )
