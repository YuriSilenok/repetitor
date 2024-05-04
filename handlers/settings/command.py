"""Обработка настроек"""
import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from models import ScheduleTemplate, User
from keyboards.settings import kb_week_menu, kb_yes_no
from states.settings import SettingsStates
from . import constants


NAME_PATTERN = r'_([А-я]+)$'

router = Router()

@router.message(Command('settings'))
async def settings_handler(message: Message, state: FSMContext):
    '''Обработка команды settings'''
    user = User.get(telegram_id=message.from_user.id)
    await state.set_state(SettingsStates.select_week)
    send_message = await message.answer(
        text='Это настройки для репетитора. \
Здесь Вы можете задать расписание для ваших занятий. \
Это позволит Вашим ученикам забронировать свободное время для занятия. \
В столбце `Д.Нед` Вы можете выбрать дни, в которые вы хотите проводить занятия. \
В столбце `Раб.вр` Вы можете указать рабочее время для всей недели или индивидуально для каждого дня. \
Если кликнуть по названию столбца, то время будет установлено для всей недели. \
В столбце `Обед` Вы можете задать время перерыва для всей недели или индивидуально для каждого дня. \
В столбце `Перер` Вы можете задать перерыв между занятиями для всей недели или индивидуально для \
каждого дня.'.replace('.', r'\.'),
        reply_markup=await kb_week_menu(user=user),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await state.update_data(settings_message_id=send_message.message_id)

@router.callback_query(SettingsStates.select_week and F.data=='week_day_header')
async def week_day_header_handler(callback: CallbackQuery):
    '''Справка по столбцу'''
    await callback.answer('День недели')

@router.callback_query(SettingsStates.select_week and F.data=='work_time_header')
async def work_time_header_handler(callback: CallbackQuery):
    '''Справка по столбцу'''
    await callback.answer('Рабочее время')
    await callback.message.answer(
        text='Установить единое рабочее время для всех дней недели?',
        reply_markup=await kb_yes_no('work_time_header')
    )

@router.callback_query(SettingsStates.select_week and F.data=='lunch_time_header')
async def lunch_time_header_handler(callback: CallbackQuery):
    '''Справка по столбцу'''
    await callback.answer('Обеденное время')
    await callback.message.answer(
        text='Установить единое время обеда для всех дней недели?',
        reply_markup=await kb_yes_no('lunch_time_header')
    )

@router.callback_query(SettingsStates.select_week and F.data=='timeout_header')
async def timeout_header_handler(callback: CallbackQuery):
    '''Справка по столбцу'''
    await callback.answer('Перерыв между занятиями')
    await callback.message.answer(
        text='Установить единый перерыв для всех дней недели?',
        reply_markup=await kb_yes_no('timeout_header')
    )

@router.callback_query(SettingsStates.select_week and F.data.endswith('_no'))
async def no_handler(callback: CallbackQuery):
    '''Обработка отмены операции'''
    await callback.message.delete()

@router.callback_query(SettingsStates.select_week and F.data.startswith('schedule_week_day_'))
async def schedule_week_day_handler(callback: CallbackQuery):
    '''Включение и отключение дня'''
    match = re.search(constants.ID_PATTERN, callback.data)
    if match:
        schedule = ScheduleTemplate.get_by_id(int(match.group(1)))
        schedule.enable = not schedule.enable
        schedule.save()
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=await kb_week_menu(User.get(telegram_id=callback.from_user.id))
        )

@router.callback_query(SettingsStates.select_week and F.data == 'close_settings')
async def close_settings_handler(callback: CallbackQuery, state: FSMContext):
    '''Закрыть настройки'''
    data = await state.get_data()
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=data['settings_message_id']
    )
    await state.clear()
