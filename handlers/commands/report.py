import asyncio
from typing import Tuple

from aiogram import Bot, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, invert_f
from aiogram.types import Message

from filters.chat_f import ChatFilter
from handlers.check import AuthStatusFilter
from middlewares.message_deleter import MessageDeleterMiddleware
from middlewares.notice_admins import NoticeAdminsOnReportMiddleware

report_router = Router(name='ReportRouter')

_chat_types: Tuple[ChatType, ...] = (ChatType.GROUP, ChatType.SUPERGROUP)
report_router.message.filter(
    invert_f(AuthStatusFilter()),
    ChatFilter(*_chat_types),
)
report_router.message.middleware(NoticeAdminsOnReportMiddleware())
report_router.message.middleware(MessageDeleterMiddleware())


@report_router.message(Command('report'))
async def report_command(message: Message, bot: Bot):
    if (replied_message := message.reply_to_message) is None:
        return
    bot_reply: Message = await bot.send_message(
        chat_id=message.chat.id,
        text='Message reported',
        reply_to_message_id=replied_message.message_id,
    )
    await asyncio.sleep(delay=5)
    await bot_reply.delete()
