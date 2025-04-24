# /handlers/check.py

from aiogram import Router
from aiogram.types import Message

check_router = Router(name='CheckRouter')


@check_router.message()
async def check_message(message: Message):
    pass
