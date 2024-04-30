"""Обработка настроек"""
import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from models import EventDuration, User
from keyboards.settings import kb_settings, kb_cancel, kb_duration
from states.settings import SettingsStates


TIME_PATTERN = r'^(?:[01]?[0-9]|2[0-3]):[0-5][0-9]$'
router = Router()


@router.message(Command('settings'))
async def settings_handler(message: Message):
    '''Обработка команды settings'''
    user = User.get(telegram_id=message.from_user.id)
    durations = user.durations
    durations = [f"    - {d.minutes} минут" for d in durations]
    durations = "\n".join(durations)
    message_text = f'''Ваши настройки:
Начало рабочего дня: {user.work_day_start_time}
Окончание рабочего дня: {user.work_day_end_time}
Продолжительность встречи:
{durations}
Кнопки ниже для изменения соответсвующих настроек.'''
    await message.answer(
        text=message_text,
        reply_markup=kb_settings,
    )

@router.callback_query(F.data=='setting_cancel')
async def setting_cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка отвены изменения настройки'''
    await state.clear()
    await callback_query.message.answer(
        text='Операция отменена'
    )

@router.callback_query(F.data=='work_day_start_time')
async def work_day_start_time_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка назатия кнопки начало дня'''
    await state.set_state(SettingsStates.work_day_start_time)
    await callback_query.message.answer(
        text='Введите время начала дня',
        reply_markup=kb_cancel
    )

@router.callback_query(F.data=='work_day_end_time')
async def work_day_end_time_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка назатия кнопки окончания дня'''
    await state.set_state(SettingsStates.work_day_end_time)
    await callback_query.message.answer(
        text='Введите новое время',
        reply_markup=kb_cancel
    )

@router.callback_query(F.data=='event_duration')
async def event_duration_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка назатия кнопки продолжительность встречи'''
    await state.set_state(SettingsStates.event_duration)
    user = User.get(telegram_id=callback_query.from_user.id)
    await callback_query.message.answer(
        text='Список продолжительностей встреч',
        reply_markup=await kb_duration(user=user)
    )

DELETE_DURATION_ID_PATTERN = r'_([0-9]+)$'

@router.callback_query(SettingsStates.event_duration and F.data.startswith('delete_duration_'))
async def delete_duration_handler(callback_query: CallbackQuery, state: FSMContext):
    '''Обработка удаления продолжительности занятия'''
    await callback_query.message.delete()
    match = re.search(DELETE_DURATION_ID_PATTERN, callback_query.data)
    if not match:
        await callback_query.message.answer(
            text='Не удалось извлечь ИД продолжительности. Сообщите разработчику'
        )
        return
    duration_id = match.group(1)
    duration: EventDuration = EventDuration.get_or_none(id=duration_id)
    if not duration:
        await callback_query.message.answer(
            text='Продолжительность не найдена в БД'
        )
        return
    duration.delete_instance()
    await callback_query.message.answer(
        text='Продолжительность удалена'
    )
    await state.clear()

@router.message(SettingsStates.work_day_start_time)
async def set_time_by_start_time_work_day(message: Message, state: FSMContext):
    '''Установка начала рабочего дня'''
    if re.search(TIME_PATTERN, message.text):
        user = User.get(telegram_id=message.from_user.id)
        settings = user.settings[0]
        settings.work_day_start_time = message.text
        settings.save()
        await state.clear()
        await message.answer(text='Время записано')
    else:
        await message.answer(text='Время должно соответствовать формату "ЧЧ:ММ"')

@router.message(SettingsStates.work_day_end_time)
async def set_time_by_end_time_work_day(message: Message, state: FSMContext):
    '''Установка окончания рабочего дня'''
    if re.search(TIME_PATTERN, message.text):
        user = User.get(telegram_id=message.from_user.id)
        settings = user.settings[0]
        settings.work_day_end_time = message.text
        settings.save()
        await state.clear()
        await message.answer(text='Время записано')
    else:
        await message.answer(text='Время должно соответствовать формату "ЧЧ:ММ"')
