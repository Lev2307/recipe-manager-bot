from aiogram.filters.callback_data import CallbackData

class AddToFavouritesCallback(CallbackData, prefix="add_to_favourite"):
    recipe_id: int

class CuisineCallback(CallbackData, prefix="choose_cuisine"):
    cuisine: str
    prev_message_id: int
