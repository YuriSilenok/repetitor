"""Обработка настроек"""
import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from models import ScheduleTemplate, User, WeekDay
from keyboards.settings import kb_week_menu, kb_cancel
from states.settings import SettingsStates


TIME_PATTERN = r'^(?:[01]?[0-9]|2[0-3]):[0-5][0-9]$'
ID_PATTERN = r'_([0-9]+)$'
NAME_PATTERN = r'_([А-я]+)$'

router = Router()

@router.message(Command('settings'))
async def settings_handler(message: Message, state: FSMContext):
    '''Обработка команды settings'''
    user = User.get(telegram_id=message.from_user.id)
    schedule_templates: ScheduleTemplate = ScheduleTemplate.filter(user=user)
    week = {
        'Понедельник': {'enable': False},
        'Вторник': {'enable': False},
        'Среда': {'enable': False},
        'Четверг': {'enable': False},
        'Пятница': {'enable': False},
        'Суббота': {'enable': False},
        'Воскресенье': {'enable': False},
    }

    for schedule_template in schedule_templates:
        week[schedule_template.week_day.name]['enable'] = True
        week[schedule_template.week_day.name]['start_time'] = schedule_template.start_time
        week[schedule_template.week_day.name]['end_time'] = schedule_template.end_time

    await state.update_data(week=week)
    await state.set_state(SettingsStates.select_week)
    await message.answer(
        text='Вам нужно выбрать дни недели, в которые Вы будете провоидить занятия',
        reply_markup=await kb_week_menu(
            week=week
        ),
    )

@router.callback_query(SettingsStates.select_week and F.data.startswith('week_day_id_'))
async def select_week_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка выбора дня недели'''
    data = await state.get_data()
    week = data['week']
    week_day_name = re.search(NAME_PATTERN, callback_query.data).group(1)
    week[week_day_name]["enable"] = not week[week_day_name]["enable"]
    if not week[week_day_name]['enable'] and 'start_time' in week[week_day_name]:
        del week[week_day_name]['start_time']
        del week[week_day_name]['end_time']

    await state.update_data(week=week)
    await callback_query.message.edit_reply_markup(
        reply_markup=await kb_week_menu(week)
    )

@router.callback_query(SettingsStates.select_week and F.data=='week_day_next')
async def select_week_save_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка сохранения настройки рабочих дней'''
    data = await state.get_data()
    week_day = None
    for name, value in data['week'].items():
        if value['enable'] and 'start_time' not in value:
            week_day = name
            break

    if week_day is None:
        await callback_query.answer(
            text='Для всех дней недели время указано'
        )
        return
    await state.update_data(current_week_day=week_day)
    await state.set_state(SettingsStates.set_start_day)
    await callback_query.message.edit_text(
        text=f'Укажите время начала дня недели: {week_day}',
        reply_markup=kb_cancel
    )

@router.message(SettingsStates.set_start_day)
async def set_time_by_start_time_work_day(message: Message, state: FSMContext):
    '''Установка начала рабочего дня'''
    if re.search(TIME_PATTERN, message.text):
        data = await state.get_data()
        week = data['week']
        week[data['current_week_day']]['start_time'] = message.text
        await state.update_data(week=week)
        await state.set_state(SettingsStates.set_end_day)
        await message.answer(text='Укажите время окончания дня недели')
    else:
        await message.answer(text='Время должно соответствовать формату "ЧЧ:ММ"')

@router.message(SettingsStates.set_end_day)
async def set_time_by_end_time_work_day(message: Message, state: FSMContext):
    '''Установка окончания рабочего дня'''
    if re.search(TIME_PATTERN, message.text):
        data = await state.get_data()
        week = data['week']
        week[data['current_week_day']]['end_time'] = message.text
        await state.update_data(week=week)

        week_day = None
        for name, value in week.items():
            if value['enable'] and 'start_time' not in value:
                week_day = name
                break

        if week_day:
            await state.update_data(current_week_day=week_day)
            await state.set_state(SettingsStates.set_start_day)
            await message.answer(
                text=f'Укажите время начала дня недели: {week_day}',
                reply_markup=kb_cancel
            )
            return

        user = User.get(telegram_id=message.from_user.id)
        for name, value in week.items():
            enable = value['enable']
            week_day = WeekDay.get(name=name)
            schedule: ScheduleTemplate = ScheduleTemplate.get_or_none(
                user=user,
                week_day=week_day,
            )

            if schedule and enable:
                schedule.start_time = value['start_time']
                schedule.end_time = value['end_time']
                schedule.save()
            elif schedule and not enable:
                schedule.delete_instance()
            elif not schedule and enable:
                ScheduleTemplate.create(
                    user=user,
                    week_day=week_day,
                    start_time=value['start_time'],
                    end_time=value['end_time'],
                )

        await state.clear()
        await message.answer(
            text='Расписание сохранено.'
        )
    else:
        await message.answer(
            text='Время должно соответствовать формату "ЧЧ:ММ"'
        )

@router.callback_query(F.data=='setting_cancel')
async def setting_cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка отвены изменения настройки'''
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Настройки не сохранены!'
    )


# @router.callback_query(F.data=='work_day_start_time')
# async def work_day_start_time_handler(callback_query: CallbackQuery, state: FSMContext):
#     '''Обработка назатия кнопки начало дня'''
#     await state.set_state(SettingsStates.work_day_start_time)
#     await callback_query.message.edit_text(
#         text='Введите время начала дня',
#         reply_markup=kb_cancel
#     )

# @router.callback_query(F.data=='work_day_end_time')
# async def work_day_end_time_handler(callback_query: CallbackQuery, state: FSMContext):
#     '''Обработка назатия кнопки окончания дня'''
#     await state.set_state(SettingsStates.work_day_end_time)
#     await callback_query.message.edit_text(
#         text='Введите новое время',
#         reply_markup=kb_cancel
#     )

# @router.callback_query(F.data=='event_duration')
# async def event_duration_handler(callback_query: CallbackQuery, state: FSMContext):
#     '''Обработка назатия кнопки продолжительность встречи'''
#     await state.set_state(SettingsStates.event_duration)
#     user = User.get(telegram_id=callback_query.from_user.id)
#     await callback_query.message.edit_text(
#         text='Список продолжительностей встреч',
#         reply_markup=await kb_duration(user)
#     )

# @router.callback_query(SettingsStates.event_duration and F.data.startswith('delete_duration_'))
# async def delete_duration_handler(callback_query: CallbackQuery, state: FSMContext):
#     '''Удаление продолжительности занятия'''
#     match = re.search(DELETE_DURATION_ID_PATTERN, callback_query.data)
#     if not match:
#         await callback_query.message.answer(
#             text='Не удалось извлечь ИД продолжительности. Сообщите разработчику'
#         )
#         return
#     duration_id = match.group(1)
#     duration: EventDuration = EventDuration.get_or_none(id=duration_id)
#     if not duration:
#         await callback_query.message.answer(
#             text='Продолжительность не найдена в БД'
#         )
#         return
#     duration.delete_instance()
#     await state.clear()
#     await callback_query.message.answer(
#         text='Продолжительность удалена'
#     )

# @router.callback_query(SettingsStates.event_duration and F.data=='add_duration')
# async def add_duration_handler(callback_query: CallbackQuery, state: FSMContext):
#     '''Нажатие кнопки Добавить продолжительность занятия'''
#     await callback_query.message.delete()
#     await state.set_state(SettingsStates.add_duration)
#     await callback_query.message.answer(
#         text='Введите количество минут продолжительности занятия',
#         reply_markup=kb_cancel,
#     )

# @router.message(SettingsStates.add_duration)
# async def input_duration_handler(message: Message, state: FSMContext):
#     """Ввод времени продолжительности занятия"""
#     try:
#         duration_minutes = int(message.text)
#         if duration_minutes <= 0:
#             await message.answer(
#                 text='Продолжительность должна быть больше нуля'
#             )
#             return

#         user = User.get(telegram_id=message.from_user.id)
#         EventDuration.create(user=user, minutes=duration_minutes)
#         await state.clear()
#         await message.answer(
#             text='Продолжительность добавлена'
#         )
#         await message.answer(
#             text='Список продолжительностей встреч',
#             reply_markup=await kb_duration(user)
#         )
#     except ValueError:
#         await message.answer(
#             text='Продолжительность должна быть целым числом'
#         )

