from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from art import tprint

async def on_startup(_):
    tprint('''BOT LAUNCHED 
    SUCCESSIFULLY''', font='bulbhead')

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)