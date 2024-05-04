"""Клавиатуры для настроек"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import User

MARKS = {
    True: '✅',
    False: '❌',
    None: '✏️',
}

async def kb_week_menu(user: User):
    '''Меню для выбора рабочих дней недели'''
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Д.Нед',
                callback_data='week_day_header',
            ),
            InlineKeyboardButton(
                text='Раб.вр',
                callback_data='work_time_header',
            ),
            InlineKeyboardButton(
                text='Обед',
                callback_data='lunch_time_header',
            ),
            InlineKeyboardButton(
                text='Перер',
                callback_data='timeout_header',
            ),
        ]
    ]

    for schedule in user.schedule:
        row = [
            InlineKeyboardButton(
                text=f'{MARKS[schedule.enable]}{schedule.week_day}',
                callback_data=f'schedule_week_day_{schedule}',
            ),
        ]

        text = '??:??-??:??'
        if schedule.work_start_time and schedule.work_end_time:
            start_time = schedule.work_start_time.strftime("%H:%M")
            end_time = schedule.work_end_time.strftime("%H:%M")
            text=f'{start_time}-{end_time}'
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f'schedule_work_time_{schedule.id}'
            )
        )

        text = '??:??-??:??'
        if schedule.lunch_start_time and schedule.lunch_end_time:
            start_time = schedule.lunch_start_time.strftime("%H:%M")
            end_time = schedule.lunch_end_time.strftime("%H:%M")
            text=f'{start_time}-{end_time}'
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f'schedule_lunch_time_{schedule.id}'
            )
        )

        text = '-'
        if schedule.timeout:
            text=f'{schedule.timeout}'
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f'schedule_timeout_{schedule.id}'
            )
        )

        inline_keyboard.append(row)
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text = 'Закрыть',
                callback_data='close_settings'
            )
        ]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


async def kb_yes_no(callback_data:str):
    '''Вопрос для массовой операции по настройкам'''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да',
                    callback_data=f'{callback_data}_yes'
                ),
                InlineKeyboardButton(
                    text='Нет',
                    callback_data=f'{callback_data}_no'
                ),
            ]
        ]
    )


    # first_row = True
    # row = []
    # for key, value in week.items():
    #     text = f'{MARKS[value["enable"]]} {key}'

    #     row.append(
    #         InlineKeyboardButton(
    #             text=text,
    #             callback_data=f'week_day_id_{key}',
    #         )
    #     )
    #     if len(row) == 2 or first_row:
    #         inline_keyboard.append(row)
    #         row = []
    #         first_row = False

    # inline_keyboard.append(row)

    # inline_keyboard.append(
    #     [
    #         InlineKeyboardButton(
    #             text='Для всех',
    #             callback_data='set_time_for_all'
    #         ),
    #         InlineKeyboardButton(
    #             text='Для каждого',
    #             callback_data='set_time_for_each'
    #         ),
    #         InlineKeyboardButton(
    #             text='Для изменёных',
    #             callback_data='set_time_for_edit'
    #         ),
    #     ]
    # )
    # inline_keyboard.append(
    #     [
    #         InlineKeyboardButton(
    #             text='Отмена',
    #             callback_data='setting_cancel'
    #         ),
    #         InlineKeyboardButton(
    #             text='Сохранить',
    #             callback_data='setting_save'
    #         ),
    #     ]
    # )

    # return InlineKeyboardMarkup(
    #     inline_keyboard=inline_keyboard
    # )


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
