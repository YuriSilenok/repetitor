"""Клавиатуры для расписания"""
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import User

kb_schedule_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Найти временя для нового занятия',
            callback_data='search_event'
        ),
    ]
])

async def kb_shedule_by_teacher(user: User):
    schedule_data = {}
    for day in range(10):
        date = datetime.now().date() + timedelta(days=day)
        