import asyncio
import asyncio.mixins
import logging

from aiogram import Bot, Dispatcher

from config import bot
from app.handlers import router


dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # Испольется только при разработке, при запуске нужно отключить, ТК сильно замедляет прогу
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')