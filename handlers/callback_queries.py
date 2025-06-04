from typing import Optional

from aiogram import Bot, F, Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    CallbackQuery,
    ChatFullInfo,
    MaybeInaccessibleMessageUnion,
    Message,
)

from enums.actions import Action
from filters.admin_f import UserAdminFilter


class AdminAction(CallbackData, prefix='adm'):
    action: Action
    chat_id: int
    user_id: int
    username: str
    message_id: int


query_router: Router = Router(name='QueryRouter')

query_router.callback_query.filter(UserAdminFilter())


@query_router.callback_query(AdminAction.filter(F.action == Action.RESTORE))
async def restore(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    message: Optional[MaybeInaccessibleMessageUnion] = query.message
    if not isinstance(message, Message):
        return

    original_message: Optional[Message] = message.reply_to_message
    if original_message is None:
        return

    edited_text: str = (
        f'Restored message sended by {callback_data.username}:\n\n{original_message.html_text}'
    )

    await bot.edit_message_text(
        chat_id=callback_data.chat_id,
        message_id=callback_data.message_id,
        text=edited_text,
    )

    await query.answer(text='Сообщение восстановлено')
    await message.delete_reply_markup()


@query_router.callback_query(AdminAction.filter(F.action == Action.BAN))
async def ban(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    message: Optional[MaybeInaccessibleMessageUnion] = query.message
    if not isinstance(message, Message):
        return

    chat_info: ChatFullInfo = await bot.get_chat(chat_id=callback_data.chat_id)

    match (await chat_info.get_member(callback_data.user_id)).status:
        case ChatMemberStatus.CREATOR:
            await query.answer('Нельзя заблокировать создателя чата')
        case ChatMemberStatus.ADMINISTRATOR:
            await query.answer('Нельзя заблокировать администратора')
        case _:
            if query.from_user.id == callback_data.user_id:
                await query.answer('Нельзя заблокировать самого себя')
            else:
                await bot.ban_chat_member(
                    chat_id=callback_data.chat_id, user_id=callback_data.user_id
                )
                await bot.delete_message(
                    chat_id=callback_data.chat_id,
                    message_id=callback_data.message_id,
                )
                await query.answer(
                    text=f'Пользователь {callback_data.username} заблокирован'
                )
                await message.delete_reply_markup()
