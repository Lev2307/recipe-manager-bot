from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

def add_to_favourite():
    inline_kb_list = [
        [InlineKeyboardButton(text="Добавить к избранным рецептам", callback_data="add_to_favourites")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def countries_cuisines():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇸 Американская", callback_data="cuisine_American")
    builder.button(text="🇬🇧 Британская", callback_data="cuisine_British")
    builder.button(text="🇨🇳 Китайская", callback_data="cuisine_Chinese")
    builder.button(text="🇫🇷 Французская", callback_data="cuisine_French")
    builder.button(text="🇩🇪 Немецкая", callback_data="cuisine_German")
    builder.button(text="🇮🇹 Итальянская", callback_data="cuisine_Italian")
    builder.button(text="🇲🇽 Мексиканская", callback_data="cuisine_Mexican")
    builder.adjust(2)

    return builder.as_markup()