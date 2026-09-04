"""
Text-based interface for user interaction with the agent.
Handles input/output via terminal/console.
"""
from input.text_input import TextInput


class TextInterface:
    """
    Text-only interface for the assistant.
    """

    def __init__(self, prompt: str = "You: "):
        self.text_input = TextInput(prompt=prompt)

    def get_input(self) -> str:
        return self.text_input.read()

    def show_output(self, response: str):
        print(f"Assistant: {response}")

    def show_welcome(self, agent=None):
        print("\n" + "=" * 54)
        print("  AI Assistant  —  powered by Featherless AI")
        print("=" * 54)
        if agent and hasattr(agent, "llm_client"):
            print(f"  Active model : {agent.llm_client.get_model()}")
        print("  Type 'exit' or 'quit' to stop.")
        print("  Type 'list models' or '/models' to see all AI models.")
        print("  Type '/model <name>' to switch the active AI model.")
        print("=" * 54 + "\n")

    def show_goodbye(self):
        print("Assistant stopped.")

    def run(self, agent):
        """Main interaction loop connecting User -> TextInput -> Agent -> Decision -> Output."""
        self.show_welcome(agent)

        while True:
            user_msg = self.get_input()

            if self.text_input.is_exit_command(user_msg):
                self.show_goodbye()
                break

            if not user_msg:
                continue

            response = agent.run(user_msg)
            self.show_output(response)