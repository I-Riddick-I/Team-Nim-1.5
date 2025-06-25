# /handlers/check/check.py

from typing import Optional, Tuple, Union

from aiogram import F, Router
from aiogram.filters import Filter, or_f
from aiogram.types import Message
from aiogram.utils.magic_filter import MagicFilter

import keyboards
import keyboards.user_kb
from filters.forbidden.ai_f import ArtificialIntelligenceFilter
from filters.forbidden.badwords_f import BadwordsFilter
from filters.forbidden.urls_f import UrlFilter

_check_text_filters: Tuple[Union[Filter, MagicFilter], ...] = (
    F.text,
    or_f(
        badwords_filter := BadwordsFilter(),
        url_filter := UrlFilter(),
        ai_filter := ArtificialIntelligenceFilter(
            enable=True, retry_attempts=50
        ),
    ),
)

check_text_router = Router(name='CheckTextRouter')

check_text_router.message.filter(*_check_text_filters)
check_text_router.edited_message.filter(*_check_text_filters)


@check_text_router.message()
@check_text_router.edited_message()
async def check_text_message(message: Message) -> Optional[Message]:
    if (user := message.from_user) is None:
        return None
    return await message.answer(
        text='Сообщение на модерации',
        disable_notification=True,
        reply_markup=keyboards.user_kb.appeal_keyboard(user_id=user.id),
    )
