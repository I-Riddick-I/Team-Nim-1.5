# /handlers/commands/admin/__init__.py

from typing import Tuple

from aiogram import F, Router, html
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandStart, Filter, invert_f
from aiogram.types import Chat, Message

from filters.admin_f import UserAdminFilter
from filters.authorization_f import AuthStatusFilter
from main.configure import config as _config

from .groups import groups_router as _groups_router
from .id import id_router as _id_router

_admin_filters: Tuple[Filter, ...] = (
    UserAdminFilter(),
    invert_f(AuthStatusFilter()),
)

admin_commands_router = Router(name='AdminCommandsRouter')

admin_commands_router.include_routers(_id_router, _groups_router)

admin_commands_router.message.filter(*_admin_filters)


@admin_commands_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer('Welcome message')


@admin_commands_router.message(Command('echo'), F.text)
async def command_echo_text(message: Message) -> None:
    text: str = message.html_text
    if text is not None:
        answer_part: str = text.lstrip('/echo ')
        await message.answer(answer_part) if answer_part else None


@admin_commands_router.message(Command('status'))
async def command_status(message: Message):
    chat: Chat = message.chat
    answer_parts: list[str] = [
        f'Chat id: {html.code(str(chat.id))}',
        f'is Admins Chat exists: {_config.admins_chat is not None}',
        f'is Admins Chat: {chat.id == _config.admins_chat}',
    ]
    if chat.type != ChatType.PRIVATE:
        answer_parts.append(
            f'is Group Allowed: {chat.id in _config.allowed_groups}'
        )
    await message.answer('\n'.join(answer_parts))
