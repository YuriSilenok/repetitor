'''Обработка событий с расписанием'''

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import schedule as kb_schedule

router = Router()

@router.message(Command('schedule'))
async def schedule_handler(message: Message):
    '''Обработка команды /schedule'''
    await message.answer(
        text="Ваше расписание",
        reply_markup=kb_schedule.kb_schedule_menu
    )
