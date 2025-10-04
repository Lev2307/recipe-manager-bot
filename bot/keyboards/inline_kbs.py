from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callBacks import AddToFavouritesCallback, DeleteFromFavouritesCallback, CuisineCallback

CUISINES = [
    ['🇺🇸 Американская', 'American'], 
    ['🇬🇧 Британская', 'British'], 
    ['🇨🇳 Китайская', 'Chinese'], 
    ['🇫🇷 Французская', 'French'], 
    ['🇩🇪 Немецкая', 'German'], 
    ['🇮🇹 Итальянская', 'Italian'], 
    ['🇲🇽 Мексиканская', 'Mexican'], 
    ['🇰🇷 Корейская', 'Korean'],
]

def welcome_kbs():
    inline_kb_list = [
        [InlineKeyboardButton(text="Избранные рецепты 🍳", callback_data="get_favourite_recipes")],
        [InlineKeyboardButton(text="Найти рецепты 🔎", callback_data="search_recipes")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def favourite_recipes_kbs():
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

def add_to_favourites(recipe_id: int):
    inline_kb_list = [
        [InlineKeyboardButton(text="Добавить к избранным рецептам 📌", callback_data=AddToFavouritesCallback(recipe_id=recipe_id).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def delete_from_favourites(recipe_id: int):
    inline_kb_list = [
        [InlineKeyboardButton(text="Удалить из избранного 🗑️", callback_data=DeleteFromFavouritesCallback(recipe_id=recipe_id).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def countries_cuisines(m_id: int):
    builder = InlineKeyboardBuilder()
    for cuis in range(len(CUISINES)):
        builder.button(text=CUISINES[cuis][0], callback_data=CuisineCallback(cuisine=CUISINES[cuis][1], prev_message_id=m_id))
    builder.button(text="Вернуться на главную", callback_data="go_to_start")
    builder.adjust(2)

    return builder.as_markup()