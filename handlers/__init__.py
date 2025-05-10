# /handlers/__init__.py

from aiogram.dispatcher.router import Router

from .chat_join_request import chat_join_request_router
from .check import check_router
from .commands import commands_router

routers: list[Router] = [
    commands_router,
    check_router,
    chat_join_request_router,
]
