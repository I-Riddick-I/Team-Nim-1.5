from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware, Bot, html
from aiogram.types import Chat
from aiogram.types import LinkPreviewOptions as LPO
from aiogram.types import Message, TelegramObject, User

from filters.admin_f import IsAdminInGroup, UserAdminFilter
from keyboards.admin_kb import (
    keyboard_for_deleted_message,
    keyboard_for_reported_message,
)
from main.configure import config as _config


class NoticeAdminsOnDeletedMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(message, Message):
            return

        admins_chat_id: Optional[int] = _config.admins_chat
        if admins_chat_id is None:
            return

        bot: Optional[Bot] = message.bot
        if bot is None:
            return

        chat: Chat = message.chat
        chat_name: str = chat.full_name

        user: Optional[User] = message.from_user
        if user is None:
            return
        username: str = f'@{user.username}' if user.username else 'UnknownUser'

        # Пересылаем сообщение с потенциальными нарушениями в чат админов
        forwarded_message: Message = await message.forward(
            chat_id=admins_chat_id,
            disable_notification=True,
        )

        # Получаем сообщение - ответ бота
        # (Здесь также происходит удаление исходного сообщения)
        message_sended_by_bot = await handler(message, data)
        if not isinstance(message_sended_by_bot, Message):
            return

        notification_text_for_admins: str = '\n\n'.join(
            (
                data.pop('notice_message', 'Violations detected'),
                f'Sended by {username}',
                f'in chat: {html.link(chat_name, chat_link if (chat_link := message_sended_by_bot.get_url()) else "")}',
            )
        )

        # Отправляем сообщение с подробной информацией в чат админов
        await bot.send_message(
            chat_id=admins_chat_id,
            text=notification_text_for_admins,
            link_preview_options=LPO(is_disabled=True),
            reply_to_message_id=forwarded_message.message_id,
            disable_notification=True,
            reply_markup=keyboard_for_deleted_message(
                chat_id=chat.id,
                user_id=user.id,
                message_id=message_sended_by_bot.message_id,
            ),
        )


class NoticeAdminsOnReportMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        message: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(message, Message):
            return

        admins_chat_id: Optional[int] = _config.admins_chat
        if admins_chat_id is None:
            return

        bot: Optional[Bot] = message.bot
        if bot is None:
            return

        reported_message = message.reply_to_message
        if reported_message is None:
            return

        if (await UserAdminFilter()(reported_message)) or (
            await IsAdminInGroup()(reported_message)
        ):
            return

        user: Optional[User] = message.from_user
        if user is None:
            return

        reported_user: Optional[User] = reported_message.from_user
        if reported_user is None:
            return

        user_username: str = (
            f'@{user.username}' if user.username else 'UnknownUser'
        )
        reported_username: str = (
            f'@{reported_user.username}'
            if reported_user.username
            else 'UnknownUser'
        )

        chat: Chat = reported_message.chat
        chat_name: str = chat.full_name

        notification_text_for_admins: str = '\n\n'.join(
            (
                f'Reported message by {user_username}',
                f'Sended by {reported_username}',
                f'in chat: {html.link(chat_name, chat_link if (chat_link := reported_message.get_url()) else "")}',
            )
        )

        # Пересылаем сообщение с потенциальными нарушениями в чат админов
        forwarded_message: Message = await reported_message.forward(
            chat_id=admins_chat_id,
            disable_notification=True,
        )

        # Отправляем сообщение с подробной информацией в чат админов
        await bot.send_message(
            chat_id=admins_chat_id,
            text=notification_text_for_admins,
            link_preview_options=LPO(is_disabled=True),
            reply_to_message_id=forwarded_message.message_id,
            disable_notification=True,
            reply_markup=keyboard_for_reported_message(
                chat_id=chat.id,
                user_id=reported_user.id,
                message_id=reported_message.message_id,
            ),
        )

        await handler(message, data)
