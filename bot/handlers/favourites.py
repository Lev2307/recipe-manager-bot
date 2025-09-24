from aiogram import Router, F, Dispatcher
from aiogram.types import CallbackQuery

from keyboards.inline_kbs import fav_recipes_kbs

favourites_router = Router()

@favourites_router.callback_query(F.data == 'get_favourite_recipes')
async def get_favourite_recipes(callback_query: CallbackQuery, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favourites WHERE fav_user_id=%s", (callback_query.from_user.id, ))
    favourites = cursor.fetchall()
    if len(favourites) == 0:
        await callback_query.message.edit_text('У вас пока что нет любимых рецептов.', reply_markup=fav_recipes_kbs())