from pathlib import Path
from typing import Literal

from utils.paths import DATA_DIR

blacklist_path: Path = DATA_DIR / 'urls' / 'blacklist.txt'
whitelist_path: Path = DATA_DIR / 'urls' / 'whitelist.txt'


def load_urls_list(level: Literal['blacklist', 'whitelist']):
    path: Path
    match level:
        case 'blacklist':
            path = blacklist_path
        case 'whitelist':
            path = whitelist_path
    with open(path, mode='r') as file:
        return set(file.read().split('\n'))
