# /handlers/commands/admin/__init__.py

from typing import Optional

from aiogram import Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Chat, Message, User

from filters.admin import AdminFilter
from filters.default_text import DefaultTextMessageFilter
from main import dispatcher

admin_commands_router = Router(name='AdminCommandsRouter')

admin_commands_router.message.filter(AdminFilter())


@admin_commands_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer('Welcome message')


@admin_commands_router.message(Command('stop'))
async def command_stop(message: Message) -> None:
    user: Optional[User] = message.from_user
    if user is None:
        await message.answer('Something went wrong')
        return

    username: str = f'@{user.username}'
    userid: int = user.id

    await message.answer('Polling stopped')
    await dispatcher.stop_polling()

    print(f'Polling stopped via command /stop by user {username}, id={userid}')


@admin_commands_router.message(Command('echo'), DefaultTextMessageFilter())
async def command_echo(message: Message) -> None:
    text: Optional[str] = message.text
    if text is None:
        pass
    else:
        answer_part: str = text.lstrip('/echo ')
        await message.answer(answer_part)


@admin_commands_router.message(Command('myId'))
async def command_my_id(message: Message) -> None:
    user: Optional[User] = message.from_user
    if user is None:
        await message.answer('Something went wrong')
    else:
        await message.answer(f'Yours id: {html.code(str(user.id))}')


@admin_commands_router.message(Command('chatId'))
async def command_chat_id(message: Message) -> None:
    chat: Chat = message.chat
    await message.answer(f'Chat id: {html.code(str(chat.id))}')
