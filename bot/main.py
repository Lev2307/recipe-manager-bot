import asyncio
import logging
import sys
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from db_handlers.database import create_connection

from handlers.start import start_router
from handlers.favourites import favourites_router
from handlers.search import search_router

load_dotenv()
TOKEN = os.environ.get('TG_BOT_TOKEN')

dp = Dispatcher()

async def main():
    bot = Bot(token=TOKEN)
    conn = create_connection()
    dp["db_connection"] = conn

    dp.include_routers(start_router, favourites_router, search_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())