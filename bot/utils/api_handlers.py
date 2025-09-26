import os

from dotenv import load_dotenv
import requests

from .helpers import translate_ingredients

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

async def fetch_recipes_by_ingredients(ingredients: list, user_offset: int):
    ingredients_translated = await translate_ingredients(ingredients)
    ingredients_str = ','.join(ingredients_translated)
    url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}&ingredients={ingredients_str}&number=3&offset={user_offset}"
    response = requests.get(url)
    return response.json()
    