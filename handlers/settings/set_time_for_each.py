# '''Модуль обработки времени для измененных дней недели'''
# import re

# from aiogram import Router, F
# from aiogram.types import CallbackQuery, Message
# from aiogram.fsm.context import FSMContext
# from models import ScheduleTemplate, User
# from states.settings import SettingsStates
# from . import constants


# router = Router()


# @router.callback_query(SettingsStates.select_week and F.data=='set_time_for_each')
# async def set_time_for_each_handler(callback_query: CallbackQuery, state: FSMContext):
#     '''Нажате по кнопке Для каждого'''
#     data = await state.get_data()

#     # Сброс всех времени для всех дней
#     for _, value in data['week'].items():
#         if 'start_time' in value:
#             del value['start_time']

#     # Ищем ден недели для которого не указана дата
#     week_day = None
#     for name, value in data['week'].items():
#         if value['enable'] and 'start_time' not in value:
#             week_day = name
#             break

#     if week_day is None:
#         await callback_query.answer(
#             text='Нужно выбрать хотя бы один день недели'
#         )
#         return


#     await state.update_data(data=data)
#     await state.set_state(SettingsStates.set_lunch_time_for_all)
#     await callback_query.message.delete()
#     await callback_query.message.answer(
#         text=f'Укажите время начала дня недели: {week_day}',
#     )

# @router.message(SettingsStates.set_lunch_time_for_all)
# async def set_start_time(message: Message, state: FSMContext):
#     '''Установка начала рабочего дня'''
#     if re.search(constants.TIME_PATTERN, message.text):
#         data = await state.get_data()
#         week = data['week']
#         week[data['current_week_day']]['start_time'] = message.text
#         await state.update_data(week=week)
#         await state.set_state(SettingsStates.set_lunch_time)
#         await message.answer(text=f'Укажите время окончания дня недели: {data["current_week_day"]}')
#     else:
#         await message.answer(text='Время должно соответствовать формату "ЧЧ:ММ"')

# @router.message(SettingsStates.set_lunch_time)
# async def set_end_time(message: Message, state: FSMContext):
#     '''Установка окончания рабочего дня'''
#     if re.search(constants.TIME_PATTERN, message.text):
#         data = await state.get_data()
#         week = data['week']
#         week[data['current_week_day']]['end_time'] = message.text
#         await state.update_data(week=week)

#         week_day = None
#         for name, value in week.items():
#             if value['enable'] and 'start_time' not in value:
#                 week_day = name
#                 break

#         if week_day:
#             await state.update_data(current_week_day=week_day)
#             await state.set_state(SettingsStates.set_lunch_time_for_all)
#             await message.answer(
#                 text=f'Укажите время начала дня недели: {week_day}'
#             )
#             return

#         user = User.get(telegram_id=message.from_user.id)
#         for name, value in week.items():
#             enable = value['enable']
#             week_day = WeekDay.get(name=name)
#             schedule: ScheduleTemplate = ScheduleTemplate.get_or_none(
#                 user=user,
#                 week_day=week_day,
#             )

#             if schedule and enable:
#                 schedule.work_start_time = value['start_time']
#                 schedule.work_end_time = value['end_time']
#                 schedule.save()
#             elif schedule and not enable:
#                 schedule.delete_instance()
#             elif not schedule and enable:
#                 ScheduleTemplate.create(
#                     user=user,
#                     week_day=week_day,
#                     start_time=value['start_time'],
#                     end_time=value['end_time'],
#                 )

#         await state.clear()
#         await message.answer(
#             text='Расписание сохранено.'
#         )
#     else:
#         await message.answer(
#             text='Время должно соответствовать формату "ЧЧ:ММ"'
#         )
