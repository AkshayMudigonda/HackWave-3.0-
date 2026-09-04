"""
Executes parsed terminal commands and captures their output.
"""
import os
import subprocess


class TerminalExecutor:

    def execute(self, command):

        command_text = command["command"]

        if os.name == "nt":
            if command_text.lower() == "pwd":
                command_text = "cd"
            elif command_text.lower() == "ls":
                command_text = "dir"
            elif command_text.lower() == "clear":
                command_text = "cls"
        else:
            if command_text.lower() == "cls":
                command_text = "clear"
            elif command_text.lower() == "dir":
                command_text = "ls"

        try:
            result = subprocess.run(
                command_text,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "command": command["command"],
                "executed": command_text,
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {
                "command": command["command"],
                "executed": command_text,
                "success": False,
                "stdout": "",
                "stderr": "Command timed out.",
                "returncode": -1
            }

        except Exception as e:
            return {
                "command": command["command"],
                "executed": command_text,
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }