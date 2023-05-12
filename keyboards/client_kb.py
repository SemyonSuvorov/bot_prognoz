from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

send_loc_kb = ReplyKeyboardMarkup(resize_keyboard=True)
send_loc_kb.add(KeyboardButton(text='Отправить свою локацию🗺️', request_location=True),
                KeyboardButton(text='Отправить город'))
