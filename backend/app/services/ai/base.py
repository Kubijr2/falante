"""
The AIService abstraction called for in the project brief: everything above
this layer (TutorService, API routes, frontend) only ever talks to
AIProvider. Adding OpenAI, Claude, or Gemini support later means writing one
new file implementing this interface and registering it in factory.py —
nothing else in the app changes.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ChatMessage:
    role: str  # "system" | "user" | "assistant"
    content: str


class AIProvider(ABC):
    @abstractmethod
    def generate_reply(self, messages: list[ChatMessage]) -> str:
        """Given the full message history (including a leading system message), return the assistant's reply text."""
        ...
