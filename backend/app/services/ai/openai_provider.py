from openai import OpenAI

from app.services.ai.base import AIProvider, ChatMessage


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str, model: str):
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def generate_reply(self, messages: list[ChatMessage], json_mode: bool = False) -> str:
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            max_tokens=1200 if json_mode else 600,
            temperature=0.4,
            **kwargs,
        )
        return response.choices[0].message.content or ""
