from typing import Dict, Optional, Union

from aiogram.filters import Filter
from aiogram.types import Message
from openai import AsyncOpenAI, RateLimitError

from utils.ai_api_key import ai_api_key


class ArtificialIntelligenceFilter(Filter):
    def __init__(
        self,
        *,
        enable: bool = False,
        retry_attempts: Optional[int] = None,
    ) -> None:
        self._is_enabled: bool = enable
        self._client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=ai_api_key.get(),
        )
        self._prompt: str = (
            'Проверь есть ли в сообщении спам или токсичность, отвечай только одним словом ("Yes" / "No"):\n{message}'
        )
        self._retry_attempts: int = (
            retry_attempts
            if retry_attempts is not None and retry_attempts > 0
            else 0
        )

    @property
    def enabled(self) -> bool:
        return self._is_enabled

    def enable(self) -> None:
        self._is_enabled = True

    def disable(self) -> None:
        self._is_enabled = False

    def _update_api_key(self) -> None:
        ai_api_key.swap_to_next()
        self._client.api_key = ai_api_key.get()

    async def _get_response_from_ai(self, text: str):
        for _ in range(1 + self._retry_attempts):
            try:
                completion = await self._client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3-0324:free",
                    messages=[
                        {
                            "role": "user",
                            "content": self._prompt.format(message=text),
                        },
                    ],
                )
            except RateLimitError:
                self._update_api_key()
            else:
                return completion.choices[0].message.content
        return 'RateLimitError'

    async def __call__(self, message: Message) -> Union[bool, Dict[str, str]]:
        if not self._is_enabled:
            return False
        if message.text is None:
            return False
        match (await self._get_response_from_ai(message.text)):
            case 'Yes':
                return {"notice_message": "Violations detected by AI"}
            case 'No':
                return False
            case 'RateLimitError':
                return False
            case _:
                return False
