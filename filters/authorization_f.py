# /filters/authorization_f.py

from aiogram.filters import Filter
from aiogram.types import Message

import main.configure as _configure


class AuthStatusFilter(Filter):
    """Фильтр, проверяющий текущий статус авторизации"""

    async def __call__(self, message: Message) -> bool:
        return (_configure.auth_code is not None) and (
            not _configure.config.admins
        )
