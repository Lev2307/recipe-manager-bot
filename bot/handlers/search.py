from datetime import datetime
import math
import pytz

from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.inline_kbs import countries_cuisines, go_home_kbs
from db_handlers.database import get_user, modify_user_fields
from utils.api_handlers import fetch_recipes_by_ingredients, fetch_recipes_by_cuisine, fetch_recipe_by_id
from utils.callBacks import CuisineCallback
from .messages import send_recipe_message, send_search_message

MAX_REQUESTS_PER_DAY_FOR_UNSUB = 3
MAX_REQUESTS_PER_DAY_FOR_SUB = 10
RECIPES_NOT_FOUND_BY_INGR_MESSAGE = 'Не было найдено новых рецептов по вашим ингредиентам.'
RECIPES_NOT_FOUND_BY_CUISINE_MESSAGE = 'Не удалось найти новые рецепты по этой национальной кухне.'

class IngredientSearch(StatesGroup):
    waiting_for_ingredients = State()

search_router = Router()

@search_router.callback_query(F.data == 'search_recipes')
async def search_recipes(callback_query: CallbackQuery, dispatcher: Dispatcher):
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    conn = dispatcher["db_connection"]
    user = get_user(conn, callback_query.from_user.id)
    time_diff = math.ceil((now - user['last_search_request_time']).total_seconds() / 60.0)

    if user["is_sub"]:
        if user["count_requests_per_day"] < MAX_REQUESTS_PER_DAY_FOR_SUB:
            await send_search_message(callback_query, time_diff)
        else:
            await callback_query.message.edit_text(f'Максимальное количество запросов в день для обычного пользователя - {MAX_REQUESTS_PER_DAY_FOR_SUB}. Передохните малясь ;>', reply_markup=go_home_kbs())
    else:
        if user["count_requests_per_day"] < MAX_REQUESTS_PER_DAY_FOR_UNSUB:
           await send_search_message(callback_query, time_diff)
        else:
            await callback_query.message.edit_text(f'Максимальное количество запросов в день для продвинутого пользователя - {MAX_REQUESTS_PER_DAY_FOR_UNSUB}.', reply_markup=go_home_kbs())


@search_router.callback_query(F.data == 'search_by_ingredients')
async def search_by_ingredients(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text('Введите нужные ингредиенты через запятую. Пример ввода: курица, рис, перец')
    await state.set_state(IngredientSearch.waiting_for_ingredients)

@search_router.message(IngredientSearch.waiting_for_ingredients)
async def process_ingredients(message: Message, state: FSMContext, dispatcher: Dispatcher):
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    ingredients = message.text.split(', ')

    conn = dispatcher["db_connection"]
    user = get_user(conn, message.from_user.id)

    recipes = await fetch_recipes_by_ingredients(ingredients, user['offset_for_searching'])
    if recipes != []:
        search_message = await message.answer("⏳ Идёт поиск рецептов по выбранным ингредиентам...")
        for recipe in recipes:
            recipe_with_cooking_time = await fetch_recipe_by_id(recipe['id'])
            await send_recipe_message(message, recipe_with_cooking_time)
        if ((now - user['last_search_request_time']).total_seconds() // 8640) < 1:
            modify_user_fields(conn, user['user_id'], user['offset_for_searching'], now, user['count_requests_per_day']+1)
        else:
            modify_user_fields(conn, user['user_id'], user['offset_for_searching'], now, 1)

        await dispatcher['bot'].edit_message_text(
            chat_id=search_message.chat.id, 
            message_id=search_message.message_id, 
            text="✅ Нашёл для тебя несколько рецептов, исходя из выбранных ингредиентов."
        )
    else:
        await message.answer(RECIPES_NOT_FOUND_BY_INGR_MESSAGE)
    await state.clear()

@search_router.callback_query(F.data == 'search_by_cuisine')
async def search_by_cuisine(callback_query: CallbackQuery):
    m_id = callback_query.message.message_id
    await callback_query.message.edit_text('Какую кухню вы бы предпочли?', reply_markup=countries_cuisines(m_id))

@search_router.callback_query(CuisineCallback.filter())
async def country_cuisine(query: CallbackQuery, callback_data: CuisineCallback, dispatcher: Dispatcher):
    now = datetime.now(pytz.timezone('Europe/Moscow')) 
    cuisine_type = callback_data.cuisine

    conn = dispatcher["db_connection"]
    user = get_user(conn, query.from_user.id)

    await dispatcher["bot"].delete_message( # удаляет предыдущее сообщение с выбором 
        chat_id=query.message.chat.id,
        message_id=callback_data.prev_message_id
    )
    search_message = await query.message.answer('⏳ Идёт поиск рецептов по выбранной кухне...')
    recipes = await fetch_recipes_by_cuisine(cuisine_type, user['offset_for_searching'])
    if recipes != []:
        for recipe in recipes:
            recipe_with_ingr_and_cook_time = await fetch_recipe_by_id(recipe['id'])
            await send_recipe_message(query.message, recipe_with_ingr_and_cook_time)

        if ((now - user['last_search_request_time']).total_seconds() // 8640) < 1:
            modify_user_fields(conn, user['user_id'], user['offset_for_searching'], now, user['count_requests_per_day']+1)
        else:
            modify_user_fields(conn, user['user_id'], user['offset_for_searching'], now, 1)

        await dispatcher['bot'].edit_message_text(
            chat_id=search_message.chat.id, 
            message_id=search_message.message_id, 
            text='✅ Нашёл несколько рецептов по вашему запросу.'
        )
    else:
        await dispatcher['bot'].edit_message_text(
            chat_id=search_message.chat.id, 
            message_id=search_message.message_id, 
            text=RECIPES_NOT_FOUND_BY_CUISINE_MESSAGE
        )