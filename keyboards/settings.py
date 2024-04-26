"""Клавиатуры для настроек"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Начало дня',
                callback_data='work_day_start_time',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Конец дня',
                callback_data='work_day_end_time',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Продолжительность встечи',
                callback_data='event_duration',
            ),
        ]
    ]
)

kb_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='setting_cancel'
            )
        ]
    ]
)
