"""Пакет для обработки событий"""
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from . import start
from . import schedule
from . import settings


async def include_routers(dp:Dispatcher):
    """Подключение всех обработчиков"""

    dp.include_routers(
        start.router,
        schedule.router,
    )
    await settings.include_routers(dp)
