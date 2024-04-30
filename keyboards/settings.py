"""Клавиатуры для настроек"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import User

kb_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Начало дня',
                callback_data='work_day_start_time',
            ),
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


async def kb_duration(user: User) -> InlineKeyboardMarkup:
    '''Клавиатура для на интервалов времени в настройках'''
    inline_keyboard = []
    for duration in user.durations:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f'❌ {duration.minutes} минут',
                    callback_data=f'delete_duration_{duration.id}'
                )
            ]
        )

    inline_keyboard.extend([
        [
            InlineKeyboardButton(
                text='Отмена',
                callback_data='setting_cancel'
            ),
            InlineKeyboardButton(
                text='Добавить',
                callback_data='add_duration'
            ),
        ]
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
