# /filters/default_text.py

from aiogram.enums import ContentType
from aiogram.filters import Filter
from aiogram.types import Message


class DefaultTextMessageFilter(Filter):
    """Фильтр проверяющий является ли сообщение обычным текстом"""

    async def __call__(self, message: Message) -> bool:
        return message.content_type == ContentType.TEXT
