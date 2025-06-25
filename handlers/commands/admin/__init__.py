# /handlers/commands/admin/__init__.py

from typing import Optional, Tuple

from aiogram import Bot, F, Router, html
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, Filter, invert_f
from aiogram.types import Chat, ChatMemberUnion, Message

from filters.admin_f import UserAdminFilter
from filters.authorization_f import AuthStatusFilter
from main.configure import config as _config

from .filters import filters_router as _filters_router
from .groups import groups_router as _groups_router
from .id import id_router as _id_router

_admin_filters: Tuple[Filter, ...] = (
    UserAdminFilter(),
    invert_f(AuthStatusFilter()),
)

admin_commands_router = Router(name='AdminCommandsRouter')

admin_commands_router.include_routers(
    _id_router,
    _groups_router,
    _filters_router,
)

admin_commands_router.message.filter(*_admin_filters)


@admin_commands_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer('Use command /addGroup to handle messages in group')


@admin_commands_router.message(Command('echo'), F.text)
async def command_echo_text(message: Message) -> None:
    text: str = message.html_text
    if text is not None:
        answer_part: str = text.lstrip('/echo ')
        await message.answer(answer_part) if answer_part else None


@admin_commands_router.message(Command('info'))
async def command_info(message: Message):
    chat: Chat = message.chat
    answer_parts: list[str] = [
        f'Chat id: {html.code(str(chat.id))}',
        f'Chat type: {chat.type}',
        f'is Admins Chat exists: {"Yes" if _config.admins_chat is not None else "No"}',
        f'is Admins Chat: {"Yes" if chat.id == _config.admins_chat else "No"}',
    ]
    if chat.type != ChatType.PRIVATE:
        answer_parts.append(
            f'is Group Allowed: {"Yes" if chat.id in _config.allowed_groups else "No"}'
        )
    await message.answer('\n'.join(answer_parts), disable_notification=True)


@admin_commands_router.message(Command('adminsList'))
async def command_admins_list(message: Message, bot: Bot):
    if _config.admins_chat is None:
        return
    admins: list[str] = []
    for admin_id in _config.admins:
        try:
            chat_member: ChatMemberUnion = await bot.get_chat_member(
                chat_id=_config.admins_chat, user_id=admin_id
            )
        except TelegramBadRequest:
            admins.append(f'{admin_id}')
        else:
            username: Optional[str] = chat_member.user.username
            admins.append(f'@{username}' if username else 'UnknownUser')
    await message.answer(
        text=('Admins:\n' + '\n'.join(admins)),
        disable_notification=True,
    )
