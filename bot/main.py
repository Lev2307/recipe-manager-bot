import asyncio
import logging
import sys
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()
TOKEN = os.environ.get('TG_BOT_TOKEN')

dp = Dispatcher()

@dp.message(CommandStart())
async def welcome_handler(message: Message):
    await message.answer(f"Hello, I`m recipe manager bot 🤖")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())