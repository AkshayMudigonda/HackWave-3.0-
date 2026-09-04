"""
Filesystem tool: exposes file/directory operations to the agent.
"""
from core.results import success, failure
from tools.filesystem.parser import FilesystemParser
from tools.filesystem.safety import FilesystemSafety
from tools.filesystem.operations import FilesystemOperations


class FilesystemTool:

    def __init__(self):
        self.parser = FilesystemParser()
        self.safety = FilesystemSafety()
        self.operations = FilesystemOperations()

    def execute(self, request):

        command = (
            request.parameters.get("command")
            if isinstance(request.parameters, dict)
            else None
        ) or getattr(request, "original_input", "") or ""


        parsed = self.parser.parse(command)

        if not parsed:
            return failure(
                "Invalid filesystem command.",
                tool="filesystem",
            )

        action = parsed["action"]

        try:

            if action == "create_folder":
                path = parsed["path"]

                if not self.safety.can_create(path):
                    return failure(
                        "Folder already exists.",
                        tool="filesystem",
                        action=action,
                    )

                result = self.operations.create_folder(
                    path
                )

                return self._result(
                    result,
                    "Folder created.",
                    "Unable to create folder.",
                    action,
                )

            if action == "create_file":
                path = parsed["path"]

                if not self.safety.can_create(path):
                    return failure(
                        "File already exists.",
                        tool="filesystem",
                        action=action,
                    )

                result = self.operations.create_file(
                    path
                )

                return self._result(
                    result,
                    "File created.",
                    "Unable to create file.",
                    action,
                )

            if action == "delete":
                result = self.operations.delete(
                    parsed["path"]
                )

                return self._result(
                    result,
                    "Deleted successfully.",
                    "Unable to delete.",
                    action,
                )

            if action == "rename":
                result = self.operations.rename(
                    parsed["source"],
                    parsed["destination"],
                )

                return self._result(
                    result,
                    "Renamed successfully.",
                    "Unable to rename.",
                    action,
                )

            if action == "move":
                result = self.operations.move(
                    parsed["source"],
                    parsed["destination"],
                )

                return self._result(
                    result,
                    "Moved successfully.",
                    "Unable to move.",
                    action,
                )

            if action == "copy":
                result = self.operations.copy(
                    parsed["source"],
                    parsed["destination"],
                )

                return self._result(
                    result,
                    "Copied successfully.",
                    "Unable to copy.",
                    action,
                )

            if action == "find":
                results = self.operations.find(
                    parsed["query"]
                )

                return success(
                    str(results),
                    data=results,
                    tool="filesystem",
                    action=action,
                )

            if action == "search":
                results = self.operations.find(
                    parsed["query"]
                )

                return success(
                    str(results),
                    data=results,
                    tool="filesystem",
                    action=action,
                )

            if action == "list":
                path = parsed["path"]

                results = self.operations.list_directory(
                    path
                )

                return success(
                    str(results),
                    data=results,
                    tool="filesystem",
                    action=action,
                )

            if action == "open":
                result = self.operations.open_path(
                    parsed["path"]
                )

                return self._result(
                    result,
                    "Opened successfully.",
                    "Unable to open.",
                    action,
                )

            return failure(
                f"Unsupported filesystem action: {action}",
                tool="filesystem",
                action=action,
            )

        except Exception as exc:
            return failure(
                str(exc),
                tool="filesystem",
                action=action,
            )

    def _result(
        self,
        result,
        success_message,
        failure_message,
        action,
    ):

        if result:
            return success(
                success_message,
                tool="filesystem",
                action=action,
            )

        return failure(
            failure_message,
            tool="filesystem",
            action=action,
        )