# /handlers/commands/__init__.py

from typing import List

from aiogram import F, Router

from .admin import admin_commands_router
from .auth import auth_router
from .report import report_router

_routers: List[Router] = [
    admin_commands_router,
    auth_router,
    report_router,
]


commands_router = Router(name='CommandsRouter')

commands_router.include_routers(*_routers)

commands_router.message.filter(F.text.startswith('/'))
