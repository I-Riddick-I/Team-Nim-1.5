# /handlers/commands/admin/__init__.py

from typing import Optional, Tuple

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, Filter, invert_f
from aiogram.types import Chat, Message, User

from filters.admin_f import AdminsChatFilter, UserAdminFilter
from filters.authorization_f import AuthStatusFilter
from main.configure import config as _config
from main.init_bot import dispatcher as _dispatcher

from .id import id_router as _id_router

_admin_filters: Tuple[Filter, ...] = (
    UserAdminFilter(),
    invert_f(AuthStatusFilter()),
)

admin_commands_router = Router(name='AdminCommandsRouter')

admin_commands_router.include_routers(_id_router)

admin_commands_router.message.filter(*_admin_filters)


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
    await _dispatcher.stop_polling()

    print(f'Polling stopped via command /stop by user {username}, id={userid}')


@admin_commands_router.message(Command('echo'), F.text)
async def command_echo_text(message: Message) -> None:
    text: str = message.html_text
    if text is not None:
        answer_part: str = text.lstrip('/echo ')
        await message.answer(answer_part) if answer_part else None


@admin_commands_router.message(
    Command('setAdminsChat'), F.text, invert_f(AdminsChatFilter())
)
async def command_set_admins_chat(message: Message):
    bot: Optional[Bot] = message.bot
    if bot is None:
        await message.answer('Something went wrong')
        return

    admins_chat_id: Optional[int] = _config.admins_chat
    if admins_chat_id is not None:
        await bot.send_message(
            chat_id=admins_chat_id,
            text='This chat is no longer for admins',
        )

    chat: Chat = message.chat
    _config.admins_chat = chat.id
    _config.save()
    await message.answer('Admins chat successfully changed')
