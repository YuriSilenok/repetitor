"""Клавиатуры для расписания"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_schedule_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Добавить встречу',
            callback_data='add_event'
        ),
        InlineKeyboardButton(
            text='Запросить встречу',
            callback_data='request_event'
        ),
    ]
])
