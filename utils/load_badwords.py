import json as _json
from os.path import join as _join

DEFAULT_DIR = _join('data')


def load_words(file: str) -> list[str]:
    file_path: str = _join(DEFAULT_DIR, file)
    with open(file_path, mode='r', encoding='UTF-8') as outfile:
        return _json.loads(outfile.read())
