# filters/admin.py

from typing import Optional

from aiogram.filters import Filter
from aiogram.types import Message, User

from main.configure import config


class AdminFilter(Filter):
    """Фильтр, проверяющий является ли пользователь,
    который ввёл сообщение, администратором
    """

    async def __call__(self, message: Message) -> bool:
        user: Optional[User] = message.from_user
        return user.id in config.admins if user else False
