from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

send_loc_kb = ReplyKeyboardMarkup(resize_keyboard=True)
send_loc_kb.add(KeyboardButton(text='Отправить геолокацию🗺️', request_location=True),
                KeyboardButton(text='Отправить город'))

cancel_kb= InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Воспользоваться еще раз', callback_data='weather'),
                                      InlineKeyboardButton(text='Вернуться к меню', callback_data='cancel'))
cancel_kb_clothes= InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Воспользоваться еще раз', callback_data='clothes'),
                                      InlineKeyboardButton(text='Вернуться к меню', callback_data='cancel'))


welcome_kb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Прогноз одежды', callback_data='clothes'),
                                    InlineKeyboardButton(text='Прогноз погоды', callback_data='weather'))

stop_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
