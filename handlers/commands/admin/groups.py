# /handlers/commands/admin/groups.py

from typing import Optional, Tuple

from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, Filter, invert_f
from aiogram.types import Chat, Message
from aiogram.utils.magic_filter import MagicFilter

from filters.admin_f import AdminsChatFilter
from filters.allowed_groups_f import IsGroupAllowed
from filters.chat_f import ChatFilter
from main.configure import config as _config

_filters: Tuple[Filter | MagicFilter, ...] = (F.text,)

groups_router: Router = Router(name='GroupsRouter')

groups_router.message.filter(*_filters)


@groups_router.message(Command('setAdminsChat'), invert_f(AdminsChatFilter()))
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
    await message.answer('Admins chat successfully changed')


@groups_router.message(Command('delAdminsChat'))
async def command_del_admins_chat(message: Message):
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
        _config.admins_chat = None
        await message.answer('Admins chat successfully deleted')


@groups_router.message(
    Command('addGroup'),
    invert_f(IsGroupAllowed()),
    ChatFilter(ChatType.SUPERGROUP, ChatType.GROUP),
)
async def command_add_group(message: Message):
    _config.allowed_groups.append(message.chat.id)
    await message.answer('Group successfully added')


@groups_router.message(
    Command('removeGroup'),
    F.text,
    IsGroupAllowed(),
    ChatFilter(ChatType.SUPERGROUP, ChatType.GROUP),
)
async def command_remove_group(message: Message):
    try:
        _config.allowed_groups.remove(message.chat.id)
    except ValueError:
        await message.answer('This group is not in allowed')
    else:
        await message.answer('Group successfully removed')
