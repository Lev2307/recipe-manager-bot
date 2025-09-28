from aiogram.types import Message

from keyboards.inline_kbs import welcome_kbs, add_to_favourite
from utils.helpers import generate_ingredients_from_recipe

async def send_welcome_message(message: Message):
    await message.answer(f"Привет, я бот-менеджер рецептов 🤖. Чем могу быть полезен?", reply_markup=welcome_kbs())

async def send_recipe_message(message: Message, recipe: dict):
    ingr = await generate_ingredients_from_recipe(recipe)
    await message.answer_photo(
        photo=recipe['image'], 
        caption=f"🍽 Рецепт: {recipe['title']}\nИнгредиенты:\n{ingr}",
        reply_markup=add_to_favourite()
    )