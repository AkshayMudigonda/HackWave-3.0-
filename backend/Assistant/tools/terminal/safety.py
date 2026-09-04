"""
Terminal-specific safety checks (blocked commands, sandboxing,
confirmation triggers for destructive commands).
"""
class TerminalSafety:

    ALLOWED = {
        "python",
        "python3",
        "pip",
        "git",
        "dir",
        "ls",
        "pwd",
        "whoami",
        "ipconfig",
        "tree",
        "echo",
        "cd",
        "cls",
        "clear",
    }

    BLOCKED = {
        "shutdown",
        "format",
        "taskkill",
        "reg",
        "del",
    }

    def is_allowed(self, program: str) -> bool:

        program = program.lower().strip()

        if program in self.BLOCKED:
            return False

        return program in self.ALLOWED