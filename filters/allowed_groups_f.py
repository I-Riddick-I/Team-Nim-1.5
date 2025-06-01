from aiogram.filters import Filter
from aiogram.types import Message

from main.configure import config as _config


class IsGroupAllowed(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id in _config.allowed_groups
