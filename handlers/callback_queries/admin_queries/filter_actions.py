from typing import Optional

from aiogram import Bot, Router, html
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, MaybeInaccessibleMessageUnion, Message

import keyboards
import keyboards.admin_kb
from enums.url_filter_levels import UrlFilterLevels
from handlers.check.check_text import ai_filter, url_filter


class UrlFilterAction(CallbackData, prefix='url_filter'):
    level: UrlFilterLevels


filter_actions_router = Router(name='FilterActionsRouter')


@filter_actions_router.callback_query(UrlFilterAction.filter())
async def set_url_filter_level(
    query: CallbackQuery,
    callback_data: UrlFilterAction,
    bot: Bot,
):
    message: Optional[MaybeInaccessibleMessageUnion] = query.message
    if not isinstance(message, Message):
        return
    url_filter.change_level(callback_data.level)
    await query.answer(
        text=f'Url filter level changed to {callback_data.level.title()}'
    )
    await message.edit_text(
        text=html.bold(
            f'Current url filter level:\n{url_filter.level.title()}'
        ),
        reply_markup=keyboards.admin_kb.keyboard_for_change_url_filter_level(
            url_filter.level
        ),
    )


class AIFilterActions(CallbackData, prefix='ai_filter'):
    enable: bool


@filter_actions_router.callback_query(AIFilterActions.filter())
async def set_ai_filter_level(
    query: CallbackQuery,
    callback_data: AIFilterActions,
    bot: Bot,
):
    message: Optional[MaybeInaccessibleMessageUnion] = query.message
    if not isinstance(message, Message):
        return
    ai_filter.enable() if callback_data.enable else ai_filter.disable()
    await query.answer(
        text=f'AI filter {"enabled" if ai_filter.enabled else "disabled"}'
    )
    await message.edit_text(
        text=html.bold(
            f'AI filter {"enabled" if ai_filter.enabled else "disabled"}'
        ),
        reply_markup=keyboards.admin_kb.keyboard_for_toggle_ai_filter(
            not ai_filter.enabled
        ),
    )
