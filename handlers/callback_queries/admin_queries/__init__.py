from aiogram import Router

from filters.admin_f import UserAdminFilter

from .admin_actions import admin_actions_router
from .filter_actions import filter_actions_router

admin_query_router = Router(name='AdminQueryRouter')

admin_query_router.include_routers(
    admin_actions_router,
    filter_actions_router,
)

admin_query_router.callback_query.filter(UserAdminFilter())
