# /filters/notcommand.py

from aiogram.enums import MessageEntityType
from aiogram.filters import Filter
from aiogram.types import Message

_TYPE_BOT_COMMAND = MessageEntityType.BOT_COMMAND


class NotCommand(Filter):
    async def __call__(self, message: Message) -> bool:
        msg_entities = message.entities
        return msg_entities is None or _TYPE_BOT_COMMAND not in map(
            lambda msg_entity: msg_entity.type, msg_entities
        )
