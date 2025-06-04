# /handlers/check/check.py

from typing import Tuple, Union

from aiogram import F, Router
from aiogram.filters import Filter, or_f
from aiogram.types import Message
from aiogram.utils.magic_filter import MagicFilter

from filters.forbidden.badwords_f import BadwordsFilter
from filters.forbidden.urls_f import UrlFilter

_check_text_filters: Tuple[Union[Filter, MagicFilter], ...] = (
    F.text,
    or_f(BadwordsFilter(), UrlFilter()),
)

check_text_router = Router(name='CheckTextRouter')

check_text_router.message.filter(*_check_text_filters)
check_text_router.edited_message.filter(*_check_text_filters)


@check_text_router.message()
@check_text_router.edited_message()
async def check_text_message(message: Message) -> Message:
    return await message.answer(
        text='Сообщение на модерации',
        disable_notification=True,
    )
