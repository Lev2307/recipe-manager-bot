from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline_kbs import welcome_kbs

start_router = Router()

async def send_welcome_message(message: Message):
    await message.answer(f"Привет, я бот менеджер рецептов 🤖. Чем могу быть полезен?", reply_markup=welcome_kbs())

@start_router.message(Command('start'))
async def welcome_handler(message: Message):
    await send_welcome_message(message)

@start_router.callback_query(F.data == 'go_to_start')
async def got_to_start(callback_query: CallbackQuery):
    await callback_query.answer("Вы вернулись на главную!")
    await callback_query.message.delete()
    await send_welcome_message(callback_query.message)

