from redis.asyncio import Redis
from googletrans import Translator

r = Redis(host='redis', port=6379, db=0)

async def translate_with_cache(text: str, dest='en'):
    cached_translation = await r.get(f"translation:{text}:{dest}")
    if cached_translation:
        return cached_translation.decode('utf-8')

    async with Translator() as translator:
        translated = await translator.translate(text, dest=dest)

    await r.set(f"translation:{text}:{dest}", translated.text, ex=86400)
    return translated.text

async def translate_ingredients_to_en(ingredients: list):
    '''Translate ingredients, got from user input, from any lang to en.'''
    new_ingr_trans = []
    for i in ingredients:
        res = await translate_with_cache(i)
        new_ingr_trans.append(res)
    return new_ingr_trans

async def translate_ingredients_from_en_to_ru(ingredients: list):
    '''Translate ingredients, which have been got from api, from en to ru'''
    ingr_trans = []
    for ingr in ingredients:
        res = await translate_with_cache(ingr, dest='ru')
        ingr_trans.append(res)
    return ingr_trans

async def generate_ingredients_from_recipe(recipe: dict):
    all_ingr = list()
    if recipe.get('missedIngredients'):
        missedingr, usedingr = recipe.get('missedIngredients'), recipe.get('usedIngredients')
        all_ingr = missedingr + usedingr
    else:
        all_ingr = recipe.get('extendedIngredients')
    ingredients = [ingr['original'] for ingr in all_ingr]
    ingredients_trans = await translate_ingredients_from_en_to_ru(ingredients)
    print(ingredients_trans)
    ingredients_trans = ['• '+ingr for ingr in ingredients_trans]

    return ",\n".join(ingredients_trans)