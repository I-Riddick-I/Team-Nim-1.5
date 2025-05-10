# /filters/admin_f.py

from typing import List, Optional

from aiogram.filters import Filter
from aiogram.types import Message, ResultChatMemberUnion, User

from main.configure import config as _config


class UserAdminFilter(Filter):
    """Фильтр, проверяющий является ли пользователь,
    который ввёл сообщение, администратором
    """

    async def __call__(self, message: Message) -> bool:
        user: Optional[User] = message.from_user
        return user.id in _config.admins if user else False


class IsAdminInGroup(Filter):

    async def __call__(self, message: Message) -> bool:
        chat = message.chat

        user = message.from_user

        if user is None:
            return False
        admins_in_chat: List[ResultChatMemberUnion] = (
            await chat.get_administrators()
        )
        if (await chat.get_member(user.id)) in admins_in_chat:
            return True
        return False


class AdminsChatFilter(Filter):
    """Фильтр, проверяющий является ли чат администраторским"""

    async def __call__(self, message: Message) -> bool:
        admins_chat_id: Optional[int] = _config.admins_chat
        return message.chat.id == admins_chat_id if admins_chat_id else False
