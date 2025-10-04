from datetime import datetime

from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from keyboards.inline_kbs import welcome_kbs, add_to_favourites, delete_from_favourites
from utils.helpers import generate_ingredients_from_recipe
from utils.api_handlers import fetch_recipe_by_id

async def send_welcome_message(message: Message):
    await message.answer(f"Привет, я бот-менеджер рецептов 🤖. Чем могу быть полезен?", reply_markup=welcome_kbs())

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