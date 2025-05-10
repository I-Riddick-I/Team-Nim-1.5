# /utils/bot_token.py

from .configurator import Config as _Config


def enter_token() -> str:
    print('Get token via https://t.me/BotFather or use existing one.')
    return input('Enter bot token: ')


def clear_token(config: _Config) -> None:
    config.bot_token = ''
