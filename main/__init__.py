# /main/__init__.py

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .configure import config as _config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

bot = Bot(
    token=_config.bot_token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)

dispatcher = Dispatcher(storage=MemoryStorage())
