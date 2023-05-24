from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

send_loc_kb = ReplyKeyboardMarkup(resize_keyboard=True)
send_loc_kb.add(KeyboardButton(text='Отправить геолокацию🗺️', request_location=True),
                KeyboardButton(text='Отправить город'),
                KeyboardButton(text='Прогноз одежды'))

welcome_kb = ReplyKeyboardMarkup(resize_keyboard=True)
welcome_kb.add(KeyboardButton(text='Прогноз одежды'),
                KeyboardButton(text='Прогноз погоды'))
