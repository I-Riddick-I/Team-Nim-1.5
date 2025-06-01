# /main/configure.py

import os
from pathlib import Path
from typing import Optional

from utils.authorization import generate_code as _generate_code
from utils.bot_token import enter_token as _enter_token
from utils.configurator import Config as _Config
from utils.configurator import set_default_config as _set_default_config

PROJECT_ROOT_DIR: Path = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_DIR: Path = PROJECT_ROOT_DIR / 'configs'
CONFIG_FILE: Path = DEFAULT_CONFIG_DIR / 'config.json'


def _configure() -> None:
    if not os.path.exists(DEFAULT_CONFIG_DIR):
        os.mkdir(DEFAULT_CONFIG_DIR)

    _set_default_config(CONFIG_FILE)
    config = _Config(file_path=CONFIG_FILE)
    config.bot_token = _enter_token()
    config.save()


if __name__ == "__main__":
    _configure()
else:
    auth_code: Optional[int] = None

    config = _Config(file_path=CONFIG_FILE)

    if not config.admins:
        auth_code = _generate_code(20)

        print(f'\nAuthCode: {auth_code}')
        print(f'Use "/auth {auth_code}" in chat with bot\n')
