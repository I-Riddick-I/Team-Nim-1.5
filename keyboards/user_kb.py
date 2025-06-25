from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.callback_queries.user_actions import UserAction


def appeal_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Обжаловать',
        callback_data=UserAction(user_id=user_id),
    )

    return builder.as_markup()
