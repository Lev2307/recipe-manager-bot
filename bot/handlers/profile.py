from datetime import datetime

from aiogram import Router, F, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.enums.parse_mode import ParseMode

from db_handlers.database import get_user
from keyboards.inline_kbs import profile_kbs
from .search import MAX_REQUESTS_PER_DAY_FOR_SUB, MAX_REQUESTS_PER_DAY_FOR_UNSUB

profile_router = Router()

@profile_router.callback_query(F.data == 'profile')
async def profile(query: CallbackQuery, dispatcher: Dispatcher):
    conn = dispatcher["db_connection"]
    user = get_user(conn, query.from_user.id)
    reg_date = datetime.strftime(user["reg_date"], "%A, %B %d, %Y %I:%M %p")
    if user["is_sub"]:
        text_sub = f"✅ Подписка активка. Макс кол-во запросов в день: <b>{MAX_REQUESTS_PER_DAY_FOR_SUB}</b>"
    else:
        text_sub = f"❌ Подписки нет. Макс кол-во запросов в день: <b>{MAX_REQUESTS_PER_DAY_FOR_UNSUB}</b>"
    await query.message.edit_text(
        f"Пользователь: {user['username']}\n{text_sub}\nКоличество поисковых запросов за сегодня: {user['count_requests_per_day']}\nПользуетесь ботом с <i>{reg_date}</i>", 
        reply_markup=profile_kbs(), 
        parse_mode=ParseMode.HTML
    )
