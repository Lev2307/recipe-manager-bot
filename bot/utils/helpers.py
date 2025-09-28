from googletrans import Translator

async def translate_ingredients_to_en(ingredients: list):
    '''Translate ingredients, got from user input, from any lang to en.'''
    new_ingr_trans = []
    async with Translator() as translator:
        detected_language = await translator.detect(','.join(ingredients))
        if (detected_language.lang == 'en'):
            new_ingr_trans = ingredients.copy()
        else:
            for i in ingredients:
                res = await translator.translate(i, src=detected_language.lang, dest='en')
                new_ingr_trans.append(res.text)
    return new_ingr_trans

async def translate_ingredients_from_en_to_ru(ingredients: list):
    '''Translate ingredients, which have been got from api, from en to ru'''
    ingr_trans = []
    async with Translator() as translator:
        for ingr in ingredients:
            res = await translator.translate(ingr, src='en', dest='ru')
            ingr_trans.append(res.text)
    return ingr_trans

async def generate_ingredients_from_recipe(recipe: dict):
    ingredients, all_ingr = [], list()
    if recipe.get('missedIngredients') and recipe.get('usedIngredients'):
        missedingr = recipe.get('missedIngredients')
        usedingr = recipe.get('usedIngredients')
        all_ingr = missedingr + usedingr
    else:
        all_ingr = recipe.get('extendedIngredients')
    for ingr in all_ingr:
        ingredients.append(ingr['original'])
    ingredients_trans = await translate_ingredients_from_en_to_ru(ingredients)
    ingredients_trans = ['• ' + ingr for ingr in ingredients_trans]

    return ",\n".join(ingredients_trans)