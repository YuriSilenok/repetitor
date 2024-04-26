"""Список команд"""

from aiogram.types import BotCommand

commands = [
    BotCommand(
        command='schedule',
        description='Расписание Ваших встреч'
    ),
    BotCommand(
        command='settings',
        description='Настройки'
    )
]
