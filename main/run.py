# /main/run.py

import asyncio

from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.utils.token import TokenValidationError

from handlers import routers
from utils.bot_token import clear_token as _clear_token

from .configure import config as _config
from .init_bot import bot as _bot
from .init_bot import dispatcher as _dispatcher


async def main() -> None:
    _dispatcher.include_routers(*routers)
    await _bot.delete_webhook(drop_pending_updates=True)
    await _dispatcher.start_polling(_bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (TelegramUnauthorizedError, TokenValidationError) as error:
        _clear_token(_config)
        raise error
    except KeyboardInterrupt:
        print('Polling stopped via KeyboardInterrupt')
    finally:
        _config.save()
