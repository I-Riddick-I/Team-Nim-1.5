# /handlers/commands/admin/groups.py

from typing import Optional, Tuple

from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, Filter, invert_f
from aiogram.types import Chat, Message, User
from aiogram.utils.magic_filter import MagicFilter

from filters.admin_f import AdminsChatFilter, IsOwner, UserAdminFilter
from filters.allowed_groups_f import IsGroupAllowed
from filters.chat_f import ChatFilter
from main.configure import config as _config

_filters: Tuple[Filter | MagicFilter, ...] = (F.text, IsOwner())

groups_router: Router = Router(name='GroupsRouter')

groups_router.message.filter(*_filters)


@groups_router.message(Command('setAdminsChat'), invert_f(AdminsChatFilter()))
async def command_set_admins_chat(message: Message, bot: Bot):
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
async def command_del_admins_chat(message: Message, bot: Bot):
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


@groups_router.message(Command('addAdmin'))
async def command_add_admin(message: Message, bot: Bot):
    replied_message: Optional[Message] = message.reply_to_message
    if replied_message is None:
        return
    if await UserAdminFilter()(replied_message):
        return
    new_admin: Optional[User] = replied_message.from_user
    if new_admin is None or new_admin.is_bot:
        return
    _config.admins.append(new_admin.id)
    if _config.admins_chat is not None:
        await bot.send_message(
            chat_id=_config.admins_chat, text=f'@{new_admin.username} now admin'
        )


@groups_router.message(Command('removeAdmin'))
async def command_del_admin(message: Message, bot: Bot):
    replied_message: Optional[Message] = message.reply_to_message
    if replied_message is None:
        return
    if not (await UserAdminFilter()(replied_message)) or (
        await IsOwner()(replied_message)
    ):
        return
    admin: Optional[User] = replied_message.from_user
    if admin is None or admin.is_bot:
        return
    _config.admins.remove(admin.id)
    if _config.admins_chat is not None:
        await bot.send_message(
            chat_id=_config.admins_chat,
            text=f'@{admin.username} no longer an admin',
        )
