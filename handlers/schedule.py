'''Обработка событий с расписанием'''

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import schedule as kb_schedule
from models import Participant, User

router = Router()

@router.message(Command('schedule'))
async def schedule_handler(message: Message):
    '''Обработка команды /schedule'''
    user = User.get(telegram_id=message.from_user.id)
    participants = Participant.filter(user=user)
    if participants.count() == 0:
        await message.answer(
            text='Будущих встреч не назначено, Вы можете выбрать занятие в эти дни:'
        )
    await message.answer(
        text="Список предстоящих встреч",
        reply_markup=kb_schedule.kb_schedule_menu
    )
