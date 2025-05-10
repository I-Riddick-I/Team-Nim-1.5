from aiogram import Router
from aiogram.types import ChatJoinRequest

from filters.chat_join_request_f import IsInviteLinkCreatedByBot

chat_join_request_router: Router = Router(name='chatJoinRequestRouter')


@chat_join_request_router.chat_join_request(IsInviteLinkCreatedByBot())
async def decline_chat_join_request(chat_join_request: ChatJoinRequest):
    """Отменяет запрос на вступление в чат по ссылке, созданной ботом"""
    await chat_join_request.decline()
