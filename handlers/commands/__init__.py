# /handlers/commands/__init__.py

from typing import List

from aiogram import Router

from .admin import admin_commands_router
from .auth import auth_router

_routers: List[Router] = [
    admin_commands_router,
    auth_router,
]


commands_router = Router(name='CommandsRouter')

commands_router.include_routers(*_routers)
