"""
Text input handling: reads and normalizes user text input for the
agent loop.
"""


class TextInput:
    """
    Handles reading and preprocessing text input from the user.
    """

    def __init__(self, prompt: str = "You: "):
        self.prompt = prompt

    def read(self) -> str:
        """Read a line of input from the console."""
        try:
            raw = input(self.prompt)
            return self.normalize(raw)
        except (KeyboardInterrupt, EOFError):
            return "exit"

    def normalize(self, text: str) -> str:
        """Clean and normalize raw user input."""
        if not text:
            return ""
        return text.strip()

    def is_exit_command(self, text: str) -> bool:
        """Check if user entered an exit or quit keyword."""
        return text.lower().strip() in ("exit", "quit", "q", "bye")
