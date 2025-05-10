from typing import Optional

from aiogram.filters import Filter
from aiogram.types import ChatInviteLink, ChatJoinRequest


class IsInviteLinkCreatedByBot(Filter):
    """
    Фильтр для проверки ChatJoinRequest.
    Возвращает True если пригласительная ссылка была создана ботом.
    """

    async def __call__(self, chat_join_request: ChatJoinRequest) -> bool:
        invite_link: Optional[ChatInviteLink] = chat_join_request.invite_link
        if invite_link is None:
            return False
        elif invite_link.bot is None:
            return False
        elif invite_link.creator.id == invite_link.bot.id:
            return True
        else:
            return False
