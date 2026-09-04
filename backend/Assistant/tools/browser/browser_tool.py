"""
Browser tool: exposes web browsing/automation to the agent.
"""
from core.results import success, failure
from tools.browser.parser import BrowserParser
from tools.browser.operations import BrowserOperations


class BrowserTool:

    def __init__(self):
        self.parser = BrowserParser()
        self.operations = BrowserOperations()

    def execute(self, request):

        if request.action not in ("parse_and_execute", "parse", "open", "search"):
            return failure(
                "Unsupported browser action.",
                tool="browser",
                action=request.action,
            )

        command = request.parameters.get("command") or getattr(request, "original_input", "") or ""

        try:
            if request.action == "open" and "url" in request.parameters:
                url = request.parameters["url"]
                target = request.parameters.get("target", url)
                opened = self.operations.open(url)
                if not opened:
                    return failure(
                        "Unable to open the browser.",
                        tool="browser",
                        action="open",
                    )
                return success(
                    f"Opening {target}.",
                    data={"action": "open", "target": target, "url": url},
                    tool="browser",
                    action="open",
                )

            parsed = self.parser.parse(command)


            if parsed["action"] == "unknown":
                return failure(
                    "I could not understand the browser command.",
                    tool="browser",
                    action="parse_and_execute",
                )

            opened = self.operations.open(
                parsed["url"]
            )

            if not opened:
                return failure(
                    "Unable to open the browser.",
                    tool="browser",
                    action=parsed["action"],
                )

            if parsed["action"] == "open":
                message = (
                    f"Opening {parsed['target']}."
                )
            else:
                message = (
                    f"Opened {parsed['engine']} search results for: {parsed['query']}."
                )
                if parsed.get("requested_first_result"):
                    message += " Opening a specific result requires a configured browser automation provider."
                if parsed.get("requires_page_automation") and not parsed.get("requested_first_result"):
                    message += " Page selection, extraction, and file creation require a configured browser automation provider."

            return success(
                message,
                data=parsed,
                tool="browser",
                action=parsed["action"],
            )

        except Exception as exc:
            return failure(
                str(exc),
                tool="browser",
                action="parse_and_execute",
            )
