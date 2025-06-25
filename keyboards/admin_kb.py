from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums.actions import Action
from enums.url_filter_levels import UrlFilterLevels
from handlers.callback_queries.admin_queries.admin_actions import AdminAction
from handlers.callback_queries.admin_queries.filter_actions import (
    AIFilterActions,
    UrlFilterAction,
)


def keyboard_for_deleted_message(
    chat_id: int,
    user_id: int,
    message_id: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Восстановить',
        callback_data=AdminAction(
            action=Action.RESTORE,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
        ),
    )
    builder.button(
        text='Заблокировать',
        callback_data=AdminAction(
            action=Action.BAN,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
        ),
    )
    return builder.as_markup()


def keyboard_for_reported_message(
    chat_id: int,
    user_id: int,
    message_id: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Удалить',
        callback_data=AdminAction(
            action=Action.DELETE,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
        ),
    )
    builder.button(
        text='Заблокировать',
        callback_data=AdminAction(
            action=Action.BAN,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
        ),
    )

    return builder.as_markup()


def keyboard_for_change_url_filter_level(
    url_filter_level: UrlFilterLevels,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    for level in UrlFilterLevels:
        if level == url_filter_level:
            continue
        builder.button(
            text=level.title(), callback_data=UrlFilterAction(level=level)
        )

    return builder.as_markup()


def keyboard_for_toggle_ai_filter(enable: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=('Enable' if enable else 'Disable'),
        callback_data=AIFilterActions(enable=enable),
    )

    return builder.as_markup()
