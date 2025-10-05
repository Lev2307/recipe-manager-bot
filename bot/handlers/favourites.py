from datetime import datetime
import pytz

from aiogram import Router, F, Dispatcher
from aiogram.types import CallbackQuery

from .messages import send_favourite_recipe_message
from keyboards.inline_kbs import favourite_recipes_kbs
from utils.callBacks import AddToFavouritesCallback, DeleteFromFavouritesCallback
from db_handlers.database import get_user, add_favourite_recipe_to_user, delete_recipe_from_favourites, get_favourite_recipe, get_favourites

favourites_router = Router()

@favourites_router.callback_query(F.data == 'get_favourite_recipes')
async def get_favourite_recipes(callback_query: CallbackQuery, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]
    favourites = get_favourites(conn, callback_query.from_user.id)
    if favourites:
        for fav in favourites:
            await send_favourite_recipe_message(callback_query.message, fav['api_recipe_id'], fav['added_at'])
    else:
        await callback_query.message.edit_text('У вас пока что нет любимых рецептов.', reply_markup=favourite_recipes_kbs())

@favourites_router.callback_query(AddToFavouritesCallback.filter())
async def add_to_favourite(query: CallbackQuery, callback_data: AddToFavouritesCallback, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]
    recipe_id = callback_data.recipe_id
    user = get_user(conn, query.from_user.id)
    if not get_favourite_recipe(conn, user['user_id'], recipe_id):
        added_to_favourites_time = datetime.now(pytz.timezone('Europe/Moscow')) # added to favourites time with Moscow timezone
        add_favourite_recipe_to_user(conn, user['user_id'], recipe_id, added_to_favourites_time)
        await query.answer('Вы добавили рецепт в избранное!', show_alert=True)
    else:
        await query.answer('У вас уже есть этот рецепт в избранном!')

@favourites_router.callback_query(DeleteFromFavouritesCallback.filter())
async def delete_from_favourites(query: CallbackQuery, callback_data: DeleteFromFavouritesCallback, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]
    recipe_id = callback_data.recipe_id
    delete_recipe_from_favourites(conn, query.from_user.id, recipe_id)
    await query.answer('Вы удалили рецепт из избранного', show_alert=True)
    await query.message.delete()
    