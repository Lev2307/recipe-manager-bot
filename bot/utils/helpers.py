from googletrans import Translator

async def translate_ingredients(ingredients: list):
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