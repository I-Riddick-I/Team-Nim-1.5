# /filters/chat_f.py

from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import Message


class ChatFilter(Filter):
    """Фильтр чатов по типам."""

    def __init__(self, *types: ChatType) -> None:
        self.types = types

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.types
