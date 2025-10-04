from aiogram.filters.callback_data import CallbackData

class AddToFavouritesCallback(CallbackData, prefix="add_to_favourites"):
    recipe_id: int

class DeleteFromFavouritesCallback(CallbackData, prefix="delete_from_favourites"):
    recipe_id: int

class CuisineCallback(CallbackData, prefix="choose_cuisine"):
    cuisine: str
    prev_message_id: int
