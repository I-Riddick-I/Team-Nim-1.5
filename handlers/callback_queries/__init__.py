from aiogram import Router
from aiogram.filters import invert_f

from filters.authorization_f import AuthStatusFilter

from .admin_queries import admin_query_router
from .user_actions import user_actions_router

query_router = Router(name='QueryRouter')

query_router.include_routers(
    admin_query_router,
    user_actions_router,
)

query_router.callback_query.filter(invert_f(AuthStatusFilter()))
