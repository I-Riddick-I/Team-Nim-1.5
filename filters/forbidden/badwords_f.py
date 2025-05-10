# /filters/forbidden/banwords_f.py

from typing import Any, Dict, Optional, Union

from aiogram.filters import Filter
from aiogram.types import Message

from utils.load_badwords import load_words


class BadwordsFilter(Filter):
    _BADWORDS = load_words('badwords.json')

    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        text: Optional[str] = message.text
        if text is None:
            return False

        text = text.lower()
        for word in self._BADWORDS:
            if word in text:
                return {'notice_message': 'Badwords detected'}
        return False
