"""Пакет для обработки событий"""
from aiogram import Dispatcher
from . import set_work_time
from . import set_timeout
from . import set_lunch_time
from . import command

async def include_routers(dp:Dispatcher):
    """Подключение всех обработчиков"""
    dp.include_routers(
        command.router,
        set_work_time.router,
        set_timeout.router,
        set_lunch_time.router,
    )
