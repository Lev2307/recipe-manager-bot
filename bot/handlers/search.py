from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.inline_kbs import search_recipes_kbs
from db_handlers.database import get_user, modify_user_offset
from utils.api_handlers import fetch_recipes_by_ingredients

class IngredientSearch(StatesGroup):
    waiting_for_ingredients = State()

search_router = Router()

@search_router.callback_query(F.data == 'search_recipes')
async def search_recipes(callback_query: CallbackQuery):
    await callback_query.message.edit_text('По какому паттерну вы хотите найти рецепты?', reply_markup=search_recipes_kbs())

@search_router.callback_query(F.data == 'search_by_ingredients')
async def search_by_ingredients(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text('Введите нужные ингредиенты через запятую. Пример ввода: курица, рис, перец')
    await state.set_state(IngredientSearch.waiting_for_ingredients)

@search_router.message(IngredientSearch.waiting_for_ingredients)
async def process_ingredients(message: Message, state: FSMContext, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]
    ingredients = message.text.split(', ')
    if len(ingredients) > 0:
        user = get_user(conn, message.from_user.id)
        search_offset = user[-2]
        recipes = await fetch_recipes_by_ingredients(ingredients, search_offset)
        if recipes:
            modify_user_offset(conn, message.from_user.id, search_offset)
    await state.clear()

@search_router.callback_query(F.data == 'search_by_cuisine')
async def search_by_cuisine(callback_query: CallbackQuery):
    pass