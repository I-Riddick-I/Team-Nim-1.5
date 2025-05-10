# /filters/forbidden/urls_f.py

from typing import Any, Dict, FrozenSet, Optional, Set, Union

from aiogram.enums import MessageEntityType
from aiogram.filters import Filter
from aiogram.types import Message, MessageEntity


class UrlFilter(Filter):
    FORBIDDEN_TYPES: FrozenSet[MessageEntityType] = frozenset(
        (
            MessageEntityType.TEXT_LINK,
            MessageEntityType.URL,
        )
    )

    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        msg_entities: Optional[list[MessageEntity]] = message.entities
        if not msg_entities:
            return False
        msg_entities_types: Set[str] = set(
            map(lambda msg_entity: msg_entity.type, msg_entities)
        )
        if UrlFilter.FORBIDDEN_TYPES.intersection(msg_entities_types):
            return {"notice_message": "URL detected"}
        return False
