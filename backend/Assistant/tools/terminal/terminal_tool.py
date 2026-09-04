"""
Terminal tool: exposes shell command execution to the agent.
"""
from core.results import success, failure
from tools.terminal.parser import TerminalParser
from tools.terminal.safety import TerminalSafety
from tools.terminal.executor import TerminalExecutor


class TerminalTool:

    def __init__(self):
        self.parser = TerminalParser()
        self.safety = TerminalSafety()
        self.executor = TerminalExecutor()

    def execute(self, request):

        command = (
            request.parameters.get("command")
            if isinstance(request.parameters, dict)
            else None
        ) or getattr(request, "original_input", "") or ""


        parsed = self.parser.parse(command)

        if not parsed:
            return failure(
                "Invalid terminal command.",
                tool="terminal",
            )

        if not self.safety.is_allowed(
            parsed["program"]
        ):
            return failure(
                f"Command not allowed: {parsed['program']}",
                tool="terminal",
                action="run",
            )

        result = self.executor.execute(parsed)

        if result["success"]:

            output = result["stdout"]

            if output:
                message = output
            else:
                message = "Command executed successfully."

            return success(
                message,
                data=result,
                tool="terminal",
                action="run",
            )

        error = result["stderr"]

        return failure(
            error or "Command failed.",
            data=result,
            tool="terminal",
            action="run",
        )