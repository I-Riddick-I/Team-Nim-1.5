"""Commands to interact with filters"""

import asyncio

from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message

from handlers.check.check_text import ai_filter, url_filter
from keyboards.admin_kb import (
    keyboard_for_change_url_filter_level,
    keyboard_for_toggle_ai_filter,
)
from middlewares.message_deleter import MessageDeleterMiddleware

filters_router = Router(name='FiltersRouter')
filters_router.message.middleware(MessageDeleterMiddleware())


@filters_router.message(Command('setUrlLevel'))
async def change_url_detection_level(message: Message):
    await message.answer(
        text=html.bold(f'Current url filter level:\n{url_filter.level.value}'),
        reply_markup=keyboard_for_change_url_filter_level(url_filter.level),
    )


@filters_router.message(Command('disableAI'))
async def disable_ai_filter(message: Message):
    if not ai_filter.enabled:
        return
    ai_filter.disable()
    bot_reply = await message.answer(text=html.bold('AI filter disabled'))
    await asyncio.sleep(delay=5)
    await bot_reply.delete()


@filters_router.message(Command('enableAI'))
async def enable_ai_filter(message: Message):
    if ai_filter.enabled:
        return
    ai_filter.enable()
    bot_reply = await message.answer(text=html.bold('AI filter enabled'))
    await asyncio.sleep(delay=5)
    await bot_reply.delete()


@filters_router.message(Command('setAI'))
async def set_ai_filter(message: Message):
    await message.answer(
        text=html.bold(
            f'AI filter {"enabled" if ai_filter.enabled else "disabled"}'
        ),
        reply_markup=keyboard_for_toggle_ai_filter(not ai_filter.enabled),
    )
