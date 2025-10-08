from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode

from keyboards.inline_kbs import welcome_kbs, add_to_favourites, delete_from_favourites, search_recipes_kbs, go_home_kbs
from utils.helpers import generate_ingredients_from_recipe
from utils.api_handlers import fetch_recipe_by_id

GAP_BETWEEN_REQUESTS_IN_MINUTES = 4

async def send_welcome_message(message: Message):
    await message.answer(f"Привет, я бот-менеджер рецептов 🤖. Чем могу быть полезен?", reply_markup=welcome_kbs())

async def send_search_message(query: CallbackQuery, time_diff):
    if time_diff >= GAP_BETWEEN_REQUESTS_IN_MINUTES:
        await query.message.edit_text('По какому паттерну вы хотите найти рецепты?', reply_markup=search_recipes_kbs())
    else:
        await query.message.edit_text(f'К сожалению, вы можете искать рецепты раз в пять минут. Следующий запрос вы можете сделать через {5 - int(time_diff)} минуты ;>', reply_markup=go_home_kbs())

async def send_recipe_message(message: Message, recipe: dict):
    ingr = await generate_ingredients_from_recipe(recipe)

    await message.answer_photo(
        photo=recipe['image'], 
        caption=f"🍽 Рецепт: {recipe['title']}\nИнгредиенты:\n{ingr}\nВремя приготовления: {recipe['readyInMinutes']} минут.",
        reply_markup=add_to_favourites(recipe['id'])
    )

async def send_favourite_recipe_message(message: Message, favourite_id: int, added_at: datetime):
    recipe = await fetch_recipe_by_id(favourite_id)
    ingr = await generate_ingredients_from_recipe(recipe)
    added_at_formatted = datetime.strftime(added_at, "%A, %B %d, %Y %I:%M %p")
    await message.answer_photo(
        photo=recipe['image'], 
        caption=f"🍽 Рецепт: {recipe['title']}\nИнгредиенты:\n{ingr}\nВремя приготовления: {recipe['readyInMinutes']} минут,\nБыл добавлен в <b><i>{added_at_formatted}</i></b>",
        reply_markup=delete_from_favourites(recipe['id']),
        parse_mode=ParseMode.HTML
    )
