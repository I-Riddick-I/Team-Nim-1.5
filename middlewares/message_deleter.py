from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class MessageDeleterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(message, Message):
            return
        await message.delete()
        message_sended_by_bot = await handler(message, data)
        if not isinstance(message_sended_by_bot, Message):
            return
        return message_sended_by_bot
