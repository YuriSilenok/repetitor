'''Бот для записи на встречу'''
import asyncio
from aiogram import Bot, Dispatcher
from handlers import include_routers

bot = Bot(token='7144934541:AAHQftb4n4W41M4T1YFEe5UIzjbdbn9N_j8')
dp = Dispatcher()

async def start():
    """Запуск бота"""
    await include_routers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start())
