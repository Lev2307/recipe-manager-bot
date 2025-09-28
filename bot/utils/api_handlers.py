import os

from dotenv import load_dotenv
import requests

from .helpers import translate_ingredients_to_en

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

async def fetch_recipes_by_ingredients(ingredients: list, user_search_offset: int, recipes_number=3):
    ingredients_translated = await translate_ingredients_to_en(ingredients)
    ingredients_str = ','.join(ingredients_translated)
    url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}&ingredients={ingredients_str}&number={recipes_number}&offset={user_search_offset}"
    response = requests.get(url)
    return response.json()

async def fetch_recipes_by_cuisine(cuisine_type: str, user_search_offset: int, recipes_number=4):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&cuisine={cuisine_type}&number={recipes_number}"
    response = requests.get(url)
    return response.json().get('results', [])

async def fetch_recipe_by_id(recipe_id: int):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    response = requests.get(url)
    return response.json()