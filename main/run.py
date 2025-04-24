# /main/run.py

import asyncio

from aiogram.exceptions import TelegramUnauthorizedError

from handlers import routers
from main.configure import config as _config
from utils.bot_token import clear_token

from .init_bot import bot, dispatcher


async def main() -> None:
    dispatcher.include_routers(*routers)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except TelegramUnauthorizedError as error:
        clear_token(_config)
        raise error
    except KeyboardInterrupt:
        print('Polling stopped via KeyboardInterrupt')
    finally:
        _config.save()
