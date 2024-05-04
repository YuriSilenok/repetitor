'''Модуль установки времени для обеденных перерывов'''

import asyncio
import re
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from models import ScheduleTemplate, User
from states.settings import SettingsStates
from keyboards.settings import kb_week_menu
from . import constants

router = Router()

@router.callback_query(SettingsStates.select_week and F.data.startswith('lunch_time_header_'))
async def time_for_all_handler(callback: CallbackQuery, state: FSMContext):
    '''Опрос на получение времени'''
    await state.set_state(SettingsStates.set_lunch_time_for_all)
    await callback.message.delete()
    send_message = await callback.message.answer(
        text='Укажите время рабочего дня в формате ЧЧ:ММ-ЧЧ:ММ',
    )
    await state.update_data(del_mess_id=send_message.message_id)


@router.message(SettingsStates.set_lunch_time_for_all)
async def set_time_for_all(message: Message, state: FSMContext):
    '''Установка начала рабочего дня'''
    await message.delete()
    data = await state.get_data()
    if 'del_mess_id' in data:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=data['del_mess_id']
        )
        del data['del_mess_id']
        await state.set_data(data)
    match = re.search(constants.TIME_PATTERN, message.text)
    if match:
        for schedule in User.get(telegram_id=message.from_user.id).schedule:
            schedule.lunch_start_time = match.group(1)
            schedule.lunch_end_time = match.group(2)
            schedule.save()

        await state.set_state(SettingsStates.select_week)
        send_message = await message.answer(text='Настройки расписания сохранены!')
        await message.bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=data['settings_message_id'],
            reply_markup=await kb_week_menu(User.get(telegram_id=message.from_user.id))
        )
        await asyncio.sleep(5)
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=send_message.message_id
        )
    else:
        send_message = await message.answer(
            text='Время должно соответствовать формату "ЧЧ:ММ-ЧЧ:ММ"'
        )
        await state.update_data(del_mess_id=send_message.message_id)

@router.callback_query(SettingsStates.select_week and F.data.startswith('schedule_lunch_time_'))
async def time_handler(callback: CallbackQuery, state: FSMContext):
    '''Опрос на получение конкретного рабочего времени'''
    await state.set_state(SettingsStates.set_lunch_time)
    send_message = await callback.message.answer(
        text='Укажите время рабочего дня в формате ЧЧ:ММ-ЧЧ:ММ',
    )
    await state.update_data(del_mess_id=send_message.message_id)
    await state.update_data(
        schedule_id=int(re.search(constants.ID_PATTERN, callback.data).group(1))
    )

@router.message(SettingsStates.set_lunch_time)
async def set_time(message: Message, state: FSMContext):
    '''Установка рабочего времени'''
    await message.delete()
    data = await state.get_data()
    if 'del_mess_id' in data:
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=data['del_mess_id']
        )
        del data['del_mess_id']
        await state.set_data(data)
    match = re.search(constants.TIME_PATTERN, message.text)
    if match:
        schedule = ScheduleTemplate.get_by_id(data['schedule_id'])
        schedule.lunch_start_time = match.group(1)
        schedule.lunch_end_time = match.group(2)
        schedule.save()

        await state.set_state(SettingsStates.select_week)
        send_message = await message.answer(text='Настройки расписания сохранены!')
        await message.bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=data['settings_message_id'],
            reply_markup=await kb_week_menu(User.get(telegram_id=message.from_user.id))
        )
        await asyncio.sleep(5)
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=send_message.message_id
        )
    else:
        send_message = await message.answer(
            text='Время должно соответствовать формату "ЧЧ:ММ-ЧЧ:ММ"'
        )
        await state.update_data(del_mess_id=send_message.message_id)
