# /handlers/commands/auth.py

from typing import Optional, Tuple, Union

from aiogram import F, Router, html
from aiogram.enums import ChatType
from aiogram.filters import Command, Filter, or_f
from aiogram.types import Message, User
from magic_filter import MagicFilter

import main.configure as _configure
from filters.authorization_f import AuthStatusFilter
from filters.chat_f import ChatFilter
from middlewares.message_deleter import MessageDeleterMiddleware

_chat_types: Tuple[ChatType, ...] = (ChatType.PRIVATE,)

_auth_filters: Tuple[Union[Filter, MagicFilter], ...] = (
    ChatFilter(*_chat_types),
    AuthStatusFilter(),
    F.text,
)

auth_router = Router(name='AuthRouter')

auth_router.message.filter(*_auth_filters)

auth_router.message.middleware(MessageDeleterMiddleware())


@auth_router.message(Command('auth'))
async def auth_command(message: Message) -> None:

    user: Optional[User] = message.from_user
    text: Optional[str] = message.text

    if text is None or user is None:
        await message.answer('Something went wrong')
        return

    code_part = text.lstrip('/auth ')
    try:
        response_auth_code = int(code_part)
    except ValueError:
        await message.answer(f'Use {html.code('/auth [code]')}')
    else:
        if response_auth_code == _configure.auth_code:
            _configure.auth_code = None
            _configure.config.admins.append(user.id)
            _configure.config.admins_chat = user.id
            _configure.config.save()
            await message.answer('Success')
        else:
            await message.answer('Code is invalid')


@auth_router.message(or_f(Command('start'), Command('help')))
async def auth_start_help_command(message: Message):
    await message.answer(
        f'See {html.code("AuthCode: [code]")} in terminal and use {html.code('/auth [code]')}'
    )
