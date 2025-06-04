from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums.actions import Action
from handlers.callback_queries import AdminAction


def admin_keyboard(
    chat_id: int,
    user_id: int,
    username: str,
    message_id: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Восстановить',
        callback_data=AdminAction(
            action=Action.RESTORE,
            chat_id=chat_id,
            user_id=user_id,
            username=username,
            message_id=message_id,
        ),
    )
    builder.button(
        text='Заблокировать',
        callback_data=AdminAction(
            action=Action.BAN,
            chat_id=chat_id,
            user_id=user_id,
            username=username,
            message_id=message_id,
        ),
    )
    return builder.as_markup()
