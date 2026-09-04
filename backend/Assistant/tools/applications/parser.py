"""
Parses application launch commands into structured requests.
"""
class ApplicationParser:

    def parse(self, command: str) -> dict | None:

        text = command.strip()
        lower = text.lower()

        commands = {
            "open ": "open",
            "launch ": "open",
            "close ": "close",
            "restart ": "restart",
        }

        for prefix, action in commands.items():

            if lower.startswith(prefix):
                application = text[len(prefix):].strip()

                if not application:
                    return None

                result = {
                    "action": action,
                    "application": application,
                }
                if action == "open":
                    import re
                    match = re.match(r"(.+?)\s+(?:and\s+)?(?:write|type)\s+[\"“](.+?)[\"”]\s*$", application, re.I)
                    if match:
                        result["application"] = match.group(1).strip()
                        result["text"] = match.group(2)
                return result

        return None
