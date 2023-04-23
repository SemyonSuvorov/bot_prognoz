from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
open_weather_token = os.getenv('OWTOKEN')