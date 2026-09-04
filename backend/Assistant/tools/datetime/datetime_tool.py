"""
Datetime tool: provides current date/time and date arithmetic utilities.
"""
from core.results import success, failure
from tools.datetime.datetime import DateTime


class DateTimeTool:

    def __init__(self):
        self.datetime = DateTime()

    def execute(self, request):

        if request.action != "get":
            return failure(
                "Unsupported datetime action.",
                tool="datetime",
                action=request.action,
            )

        try:
            query = request.parameters.get(
                "query",
                "",
            )

            result = self.datetime.get(query)

            return success(
                result,
                data=result,
                tool="datetime",
                action="get",
            )

        except Exception as exc:
            return failure(
                str(exc),
                tool="datetime",
                action="get",
            )