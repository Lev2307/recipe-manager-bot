from aiogram import Router, F, Dispatcher
from aiogram.types import CallbackQuery

from keyboards.inline_kbs import favourite_recipes_kbs
from utils.callBacks import AddToFavouritesCallback
from db_handlers.database import get_user, add_favourite_recipe_to_user, get_favourite_recipe

favourites_router = Router()

@favourites_router.callback_query(F.data == 'get_favourite_recipes')
async def get_favourite_recipes(callback_query: CallbackQuery, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favourites WHERE fav_user_id=%s", (callback_query.from_user.id, ))
    favourites = cursor.fetchall()
    if len(favourites) == 0:
        await callback_query.message.edit_text('У вас пока что нет любимых рецептов.', reply_markup=favourite_recipes_kbs())

@favourites_router.callback_query(AddToFavouritesCallback.filter())
async def add_to_favourite(query: CallbackQuery, callback_data: AddToFavouritesCallback, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]
    recipe_id = callback_data.recipe_id
    user = get_user(conn, query.from_user.id)
    if not get_favourite_recipe(conn, user[1], recipe_id):
        add_favourite_recipe_to_user(conn, user[1], recipe_id)
        await query.answer('Вы добавили рецепт в избранное!')
    else:
        await query.answer('У вас уже есть этот рецепт в избранном!')