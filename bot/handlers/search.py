from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery

from keyboards.inline_kbs import search_recipes_kbs

search_router = Router()

@search_router.callback_query(F.data == 'search_recipes')
async def search_recipes(callback_query: CallbackQuery):
    await callback_query.message.edit_text('По какому паттерну вы хотите найти рецепты?', reply_markup=search_recipes_kbs())

@search_router.callback_query(F.data == 'search_by_ingredients')
async def search_by_ingredients(callback_query: CallbackQuery):
    pass

@search_router.callback_query(F.data == 'search_by_cuisine')
async def search_by_cuisine(callback_query: CallbackQuery):
    pass