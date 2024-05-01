"""Пакет для обработки событий"""
from aiogram import Dispatcher
from . import set_work_time
from . import set_time_for_each
from . import set_time_for_edit
from . import command

async def include_routers(dp:Dispatcher):
    """Подключение всех обработчиков"""
    dp.include_routers(
        command.router,
        set_work_time.router,
        set_time_for_each.router,
        set_time_for_edit.router,
    )
