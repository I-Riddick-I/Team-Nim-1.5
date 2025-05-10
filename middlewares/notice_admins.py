from typing import Any, Awaitable, Callable, Dict, List, Optional

from aiogram import BaseMiddleware, Bot, html
from aiogram.types import (
    Chat,
    LinkPreviewOptions,
    Message,
    TelegramObject,
    User,
)

from main.configure import config as _config


class NoticeAdminsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return
        message: Message = event

        admins_chat_id: Optional[int] = _config.admins_chat
        if admins_chat_id is None:
            return

        bot: Optional[Bot] = message.bot
        if bot is None:
            return

        chat: Chat = message.chat
        chat_name: str = chat.full_name
        chat_link: str
        if chat.invite_link is None:
            chat_link = (
                await chat.create_invite_link(
                    name=f'{message.message_id} {(await bot.me()).full_name}',
                    creates_join_request=True,
                )
            ).invite_link

        else:
            chat_link = chat.invite_link

        user: Optional[User] = message.from_user
        username: str = f'@{user.username}' if user else 'UnknownUser'

        notice_message: Optional[str] = data.pop('notice_message', None)

        if notice_message is not None:
            # Пересылаем сообщение с потенциальными нарушениями в чат админов
            forwarded_message: Message = await message.forward(
                chat_id=admins_chat_id,
                disable_notification=True,
            )

            notification_text_parts: List[str] = [
                notice_message + '\n',
                f'Sended by {username}\n',
                f'in chat: {html.link(chat_name, chat_link)}\n',
            ]

            notification_text_for_admins: str = '\n'.join(
                notification_text_parts
            )

            # Отправляем сообщение с подробной информацией в чат админов
            await bot.send_message(
                chat_id=admins_chat_id,
                text=notification_text_for_admins,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                reply_to_message_id=forwarded_message.message_id,
                disable_notification=True,
            )

        await handler(message, data)
