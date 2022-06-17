from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from Sqlite3 import *

loop = asyncio.get_event_loop()
TOKEN = '2096015631:AAHHMQlLzbNQc342AwOLQdRfZWwLd38zdP0'
bot = Bot(TOKEN,parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())
db = SQLighter('db.db')


if __name__ =="__main__":
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)
