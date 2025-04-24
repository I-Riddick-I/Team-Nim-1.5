# /handlers/commands/auth.py

from typing import Optional

from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Chat, Message, User

import main
from main.configure import auth_code, config

auth_router = Router(name='AuthRouter')


@auth_router.message(Command('auth'))
async def auth_command(message: Message) -> None:

    # Команда доступна только когда список админов пуст
    if config.admins:
        return

    chat: Chat = message.chat
    user: Optional[User] = message.from_user

    # команда доступна только в личном чате с ботом
    if user is not None and user.id != chat.id:
        return

    text: Optional[str] = message.text

    if text is None or user is None:
        await message.answer('Something went wrong')
        return

    code_part = text.lstrip('/auth ')
    try:
        user_auth_code = int(code_part)
    except ValueError:
        await message.answer(f'Use {html.code('/auth [code]')}')
    else:
        if user_auth_code == auth_code:
            main.configure.auth_code = None
            config.admins.append(user.id)
            config.save()
            await message.answer('Success')
        else:
            await message.answer('Code is invalid')
