from typing import Optional

from aiogram import Bot, F, Router
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    CallbackQuery,
    MaybeInaccessibleMessageUnion,
    Message,
    ResultChatMemberUnion,
    User,
)

from enums.actions import Action

admin_actions_router = Router(name='AdminActionsRouter')


class AdminAction(CallbackData, prefix='adm'):
    action: Action
    chat_id: int
    user_id: int
    message_id: int


@admin_actions_router.callback_query(
    AdminAction.filter(F.action == Action.RESTORE)
)
async def restore(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    message: Optional[MaybeInaccessibleMessageUnion] = query.message
    if not isinstance(message, Message):
        return

    original_message: Optional[Message] = message.reply_to_message
    if original_message is None:
        return

    author_of_original_message: User = (
        await bot.get_chat_member(
            chat_id=callback_data.chat_id, user_id=callback_data.user_id
        )
    ).user

    author_username: str = (
        f'@{username}'
        if (username := author_of_original_message.username) is not None
        else 'UnknownUser'
    )

    edited_text: str = (
        f'Restored message sended by {author_username}:\n\n{original_message.html_text}'
    )

    await bot.edit_message_text(
        chat_id=callback_data.chat_id,
        message_id=callback_data.message_id,
        text=edited_text,
    )

    await query.answer(text='Сообщение восстановлено')
    await message.delete_reply_markup()


@admin_actions_router.callback_query(AdminAction.filter(F.action == Action.BAN))
async def ban(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    message: Optional[MaybeInaccessibleMessageUnion] = query.message
    if not isinstance(message, Message):
        return

    chat_member: ResultChatMemberUnion = await bot.get_chat_member(
        chat_id=callback_data.chat_id, user_id=callback_data.user_id
    )
    match chat_member.status:
        case ChatMemberStatus.CREATOR:
            await query.answer('Нельзя заблокировать создателя чата')
        case ChatMemberStatus.ADMINISTRATOR:
            await query.answer('Нельзя заблокировать администратора')
        case _ if query.from_user.id == callback_data.user_id:
            await query.answer('Нельзя заблокировать самого себя')
        case _:
            await bot.ban_chat_member(
                chat_id=callback_data.chat_id, user_id=callback_data.user_id
            )
            try:
                await bot.delete_message(
                    chat_id=callback_data.chat_id,
                    message_id=callback_data.message_id,
                )
            except TelegramBadRequest:
                pass
            author_username: str = (
                username
                if (username := chat_member.user.username) is not None
                else 'UnknownUser'
            )
            await query.answer(
                text=f'Пользователь {author_username} заблокирован'
            )
            await message.delete_reply_markup()


@admin_actions_router.callback_query(
    AdminAction.filter(F.action == Action.DELETE)
)
async def delete(query: CallbackQuery, callback_data: AdminAction, bot: Bot):
    message: Optional[MaybeInaccessibleMessageUnion] = query.message
    if not isinstance(message, Message):
        return

    chat_member: ResultChatMemberUnion = await bot.get_chat_member(
        chat_id=callback_data.chat_id, user_id=callback_data.user_id
    )
    match chat_member.status:
        case ChatMemberStatus.CREATOR:
            await query.answer('Нельзя удалить сообщение создателя чата')
        case ChatMemberStatus.ADMINISTRATOR:
            await query.answer('Нельзя удалить сообщение администратора')
        case _ if query.from_user.id == callback_data.user_id:
            await query.answer('Нельзя удалить своё сообщение')
        case _:
            try:
                await bot.delete_message(
                    chat_id=callback_data.chat_id,
                    message_id=callback_data.message_id,
                )
            except TelegramBadRequest:
                await query.answer(text='Сообщение не может быть удалено')
            else:
                author_username: str = (
                    username
                    if (username := chat_member.user.username) is not None
                    else 'UnknownUser'
                )
                await query.answer(
                    text=f'Сообщение пользователя {author_username} удалено'
                )
                await message.delete_reply_markup()
