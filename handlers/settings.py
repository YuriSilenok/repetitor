"""Обработка настроек"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from models import Settings, EventDuration, User
from keyboards.settings import kb_settings, kb_cancel
from states.settings import SettingsStates

router = Router()


@router.message(Command('settings'))
async def settings_handler(message: Message):
    '''Обработка команды settings'''
    user = User.get(telegram_id=message.from_user.id)
    settings: Settings = Settings.get(user=user)
    durations = EventDuration.filter(settings=settings)
    durations = [f"    - {d.minutes} минут" for d in durations]
    durations = "\n".join(durations)
    message_text = f'''Ваши настройки:
Начало рабочего дня: {settings.work_day_start_time}
Окончание рабочего дня: {settings.work_day_end_time}
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
        text='Введите новое время',
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
