"""
Parses raw command strings into structured commands for execution.
"""
class TerminalParser:

    def parse(self, command: str) -> dict | None:

        text = command.strip()

        if text.lower().startswith("run "):
            command_text = text[4:].strip()

        elif text.lower().startswith("execute "):
            command_text = text[8:].strip()

        else:
            command_text = text

        if not command_text:
            return None

        parts = command_text.split(maxsplit=1)

        program = parts[0]

        args = parts[1] if len(parts) > 1 else ""

        return {
            "action": "run",
            "program": program,
            "args": args,
            "command": command_text,
        }