# /handlers/commands/admin/id.py

from typing import Optional

from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import Chat, Message, User

id_router: Router = Router(name='IdRouter')

id_router.message.filter(F.text)


@id_router.message(Command('myId'))
async def command_my_id(message: Message) -> None:
    user: Optional[User] = message.from_user
    if user is None:
        await message.answer('Something went wrong')
    else:
        username: str = f'@{user.username}' if user.username else 'UnknownUser'
        await message.answer(f'{username} id: {html.code(str(user.id))}')


@id_router.message(Command('chatId'))
async def command_chat_id(message: Message) -> None:
    chat: Chat = message.chat
    await message.answer(f'Chat id: {html.code(str(chat.id))}')
