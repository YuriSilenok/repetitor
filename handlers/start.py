"""Обработка команды старт"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from models import User, EventDuration
from keyboards.start import commands


router = Router()

@router.message(Command('start'))
async def start_handler(message: Message):
    '''Обработка камандый /start'''
    user, created = User.get_or_create(telegram_id=message.from_user.id)
    if created:
        EventDuration.create(user=user)

    await message.bot.set_my_commands(commands=commands)
    await message.answer(
        text='Привет!'
    )
