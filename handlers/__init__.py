"""Пакет для обработки событий"""
from aiogram import Dispatcher
from handlers import start, schedule, settings


async def include_routers(dp:Dispatcher):
    """Подключение всех обработчиков"""
    dp.include_routers(
        start.router,
        schedule.router,
        settings.router
    )
