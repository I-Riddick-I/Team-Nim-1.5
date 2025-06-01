# /handlers/check/__init__.py

from typing import Tuple

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Filter, invert_f

from filters.admin_f import UserAdminFilter
from filters.allowed_groups_f import IsGroupAllowed
from filters.chat_f import ChatFilter
from middlewares.message_deleter import MessageDeleterMiddleware
from middlewares.notice_admins import NoticeAdminsMiddleware

from .check_text import check_text_router

_chat_types: Tuple[ChatType, ...] = (
    ChatType.GROUP,
    ChatType.SUPERGROUP,
)

_check_filters: Tuple[Filter, ...] = (
    ChatFilter(*_chat_types),
    IsGroupAllowed(),
    invert_f(UserAdminFilter()),
)


check_router = Router(name='CheckRouter')


check_router.include_routers(check_text_router)


check_router.message.filter(*_check_filters)
check_router.edited_message.filter(*_check_filters)


check_router.message.middleware(NoticeAdminsMiddleware())
check_router.edited_message.middleware(NoticeAdminsMiddleware())

check_router.message.middleware(MessageDeleterMiddleware())
check_router.edited_message.middleware(MessageDeleterMiddleware())
