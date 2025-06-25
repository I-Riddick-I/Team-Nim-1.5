# /filters/forbidden/urls_f.py

from typing import Any, Dict, FrozenSet, Set, Union

from aiogram.enums import MessageEntityType
from aiogram.filters import Filter
from aiogram.types import Message

from enums.url_filter_levels import UrlFilterLevels
from main.configure import config as _config
from utils.load_url_lists import load_urls_list


class UrlFilter(Filter):
    FORBIDDEN_TYPES: FrozenSet[MessageEntityType] = frozenset(
        (
            MessageEntityType.TEXT_LINK,
            MessageEntityType.URL,
        )
    )

    _blacklist: Set[str]
    _whitelist: Set[str]

    def __init__(self) -> None:
        try:
            self._level = UrlFilterLevels(_config.url_filter_level)
        except ValueError:
            self._level = UrlFilterLevels.OFF
        self._blacklist = load_urls_list('blacklist')
        self._whitelist = load_urls_list('whitelist')

    @property
    def level(self) -> UrlFilterLevels:
        return self._level

    def change_level(self, level: UrlFilterLevels):
        self._level = level
        _config.url_filter_level = level.value

    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        match self._level:
            case UrlFilterLevels.OFF:
                return False
            case UrlFilterLevels.BLACKLIST:
                for entity in message.entities if message.entities else ():
                    if entity.type not in UrlFilter.FORBIDDEN_TYPES:
                        continue
                    elif entity.url and entity.url[:-1] in self._blacklist:
                        return {"notice_message": "URL detected"}
                    elif message.text and entity.type == MessageEntityType.URL:
                        url_area: str = message.text[
                            entity.offset : entity.offset + entity.length
                        ]
                        if url_area in self._blacklist:
                            return {"notice_message": "URL detected"}
            case UrlFilterLevels.WHITELIST:
                for entity in message.entities if message.entities else ():
                    if entity.type not in UrlFilter.FORBIDDEN_TYPES:
                        continue
                    elif entity.url in self._whitelist:
                        return {"notice_message": "URL detected"}
                    elif message.text and entity.type == MessageEntityType.URL:
                        url_area = message.text[
                            entity.offset : entity.offset + entity.length
                        ]
                        if url_area in self._whitelist:
                            return {"notice_message": "URL detected"}
            case UrlFilterLevels.ALL:
                for entity in message.entities if message.entities else ():
                    if entity.type in UrlFilter.FORBIDDEN_TYPES:
                        return {"notice_message": "URL detected"}
        return False
