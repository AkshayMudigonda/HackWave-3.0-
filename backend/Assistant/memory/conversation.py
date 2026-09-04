"""
Stores and retrieves conversation turns (user/assistant messages).
"""
from dataclasses import dataclass
from typing import List
from memory.storage import MemoryStorage


@dataclass
class ConversationTurn:
    role: str  # "user" or "assistant"
    content: str


class ConversationMemory:
    """Manages conversation turns in memory."""

    def __init__(self, storage: MemoryStorage = None):
        self.storage = storage or MemoryStorage()
        self.turns: List[ConversationTurn] = []

    def add_user_message(self, message: str):
        self.turns.append(ConversationTurn(role="user", content=message))

    def add_assistant_message(self, message: str):
        self.turns.append(ConversationTurn(role="assistant", content=message))

    def get_history(self) -> List[ConversationTurn]:
        return list(self.turns)

    def clear(self):
        self.turns.clear()
