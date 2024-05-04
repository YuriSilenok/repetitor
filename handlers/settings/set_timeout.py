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

@router.callback_query(SettingsStates.select_week and F.data.startswith('timeout_header_'))
async def time_for_all_handler(callback: CallbackQuery, state: FSMContext):
    '''Опрос на получение времени'''
    await state.set_state(SettingsStates.set_timeout_for_all)
    await callback.message.delete()
    send_message = await callback.message.answer(
        text='Укажите продолжительность перерывов в минутах',
    )
    await state.update_data(del_mess_id=send_message.message_id)


@router.message(SettingsStates.set_timeout_for_all)
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
    match = re.search(constants.COUNT_PATTERN, message.text)
    if match:
        timeout = int(message.text)
        for schedule in User.get(telegram_id=message.from_user.id).schedule:
            schedule.timeout = timeout
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
            text='Продолжительность должна быть целым числом большим или равным нулю')
        await state.update_data(del_mess_id=send_message.message_id)

@router.callback_query(SettingsStates.select_week and F.data.startswith('schedule_timeout_'))
async def time_handler(callback: CallbackQuery, state: FSMContext):
    '''Опрос на получение конкретного рабочего времени'''
    await state.set_state(SettingsStates.set_timeout)
    send_message = await callback.message.answer(
        text='Укажите продолжительность перерыва в минутах',
    )
    await state.update_data(del_mess_id=send_message.message_id)
    await state.update_data(
        schedule_id=int(re.search(constants.ID_PATTERN, callback.data).group(1))
    )

@router.message(SettingsStates.set_timeout)
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
    match = re.search(constants.COUNT_PATTERN, message.text)
    if match:
        timeout = int(message.text)
        schedule = ScheduleTemplate.get_by_id(data['schedule_id'])
        schedule.timeout = timeout
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
            text='Продолжительность должна быть целым числом большим или равным нулю'
        )
        await state.update_data(del_mess_id=send_message.message_id)
