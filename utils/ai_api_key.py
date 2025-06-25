from os import PathLike
from typing import List

from utils.paths import DATA_DIR


def load_ai_api_keys(filepath: PathLike) -> List[str]:
    with open(filepath, mode='r') as outfile:
        return outfile.read().split('\n')


filepath = DATA_DIR / 'ai_api_keys.txt'

_AI_API_KEYS: List[str] = (
    load_ai_api_keys(filepath) if filepath.exists() else []
)


class _AIApiKey:
    def __init__(self) -> None:
        self._index = 0
        self._current_key: str = _AI_API_KEYS[self._index]

    def swap_to_next(self) -> None:
        self._index += 1
        self._index %= len(_AI_API_KEYS)
        self._current_key = _AI_API_KEYS[self._index]

    def get(self) -> str:
        return self._current_key


ai_api_key = _AIApiKey()
