"""
Parses filesystem operation commands into structured requests.
"""
class FilesystemParser:

    def parse(self, command: str) -> dict | None:

        text = command.strip()
        lower = text.lower()

        if lower.startswith("create folder "):
            return {
                "action": "create_folder",
                "path": text[14:].strip(),
            }

        if lower.startswith("create file "):
            return {
                "action": "create_file",
                "path": text[12:].strip(),
            }

        if lower.startswith("delete "):
            return {
                "action": "delete",
                "path": text[7:].strip(),
            }

        if lower.startswith("rename "):

            value = text[7:].strip()

            if " to " not in value.lower():
                return None

            parts = value.split(" to ", 1)

            return {
                "action": "rename",
                "source": parts[0].strip(),
                "destination": parts[1].strip(),
            }

        if lower.startswith("move "):

            value = text[5:].strip()

            if " to " not in value.lower():
                return None

            parts = value.split(" to ", 1)

            return {
                "action": "move",
                "source": parts[0].strip(),
                "destination": parts[1].strip(),
            }

        if lower.startswith("copy "):

            value = text[5:].strip()

            if " to " not in value.lower():
                return None

            parts = value.split(" to ", 1)

            return {
                "action": "copy",
                "source": parts[0].strip(),
                "destination": parts[1].strip(),
            }

        if lower.startswith("find "):
            return {
                "action": "find",
                "query": text[5:].strip(),
            }

        if lower.startswith("search "):
            return {
                "action": "search",
                "query": text[7:].strip(),
            }

        if lower.startswith("list "):
            return {
                "action": "list",
                "path": text[5:].strip(),
            }

        if lower.startswith("open "):
            return {
                "action": "open",
                "path": text[5:].strip(),
            }

        return None