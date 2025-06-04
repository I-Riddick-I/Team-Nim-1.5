from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware, Bot, html
from aiogram.types import Chat
from aiogram.types import LinkPreviewOptions as LPO
from aiogram.types import Message, TelegramObject, User

from keyboards.admin_kb import admin_keyboard
from main.configure import config as _config


class NoticeAdminsMiddleware(BaseMiddleware):
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

        notice_message: str = data.pop('notice_message', 'Violations detected')

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

        link_to_chat_by_message: Optional[str] = message_sended_by_bot.get_url()
        notification_text_for_admins: str = '\n\n'.join(
            (
                notice_message,
                f'Sended by {username}',
                f'in chat: {html.link(chat_name, link_to_chat_by_message if link_to_chat_by_message else '')}',
            )
        )

        # Отправляем сообщение с подробной информацией в чат админов
        await bot.send_message(
            chat_id=admins_chat_id,
            text=notification_text_for_admins,
            link_preview_options=LPO(is_disabled=True),
            reply_to_message_id=forwarded_message.message_id,
            disable_notification=True,
            reply_markup=admin_keyboard(
                chat_id=chat.id,
                user_id=user.id,
                username=username,
                message_id=message_sended_by_bot.message_id,
            ),
        )
