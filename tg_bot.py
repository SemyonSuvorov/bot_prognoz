from aiogram.utils import executor
from create_bot import dp
from handlers import admin, client
from art import tprint
from data_base import sqlite_db

async def on_startup(_):
    sqlite_db.sql_start()
    tprint('''BOT LAUNCHED 
    SUCCESSIFULLY''', font='bulbhead')
    

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)