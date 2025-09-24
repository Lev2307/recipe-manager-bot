from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def welcome_kbs():
    inline_kb_list = [
        [InlineKeyboardButton(text="Избранные рецепты 🍳", callback_data="get_favourite_recipes")],
        [InlineKeyboardButton(text="Найти рецепты 🔎", callback_data="search_recipes")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def fav_recipes_kbs():
    inline_kb_list = [
        [InlineKeyboardButton(text="Найти рецепты 🔎", callback_data="search_recipes")],
        [InlineKeyboardButton(text="Вернуться на главную", callback_data="go_to_start")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def search_recipes_kbs():
    inline_kb_list = [
        [InlineKeyboardButton(text="Поиск по ингредиентам 🍗 🔎", callback_data="search_by_ingredients")], 
        [InlineKeyboardButton(text="Поиск по национальной кухне 🍝 🔎", callback_data="search_by_cuisine")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)