from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button_load = KeyboardButton('Загрузить')
button_delete = KeyboardButton('Отмена')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load, button_delete)

colorkb = InlineKeyboardMarkup(row_width=4).add(InlineKeyboardButton(text='\U0001F3A9', callback_data='color_black'),
                                                InlineKeyboardButton(text='\U0001F407', callback_data='color_white'),
                                                InlineKeyboardButton(text='\U0001F43A', callback_data='color_grey'),
                                                InlineKeyboardButton(text='\U0001F339', callback_data='color_red'),
                                                InlineKeyboardButton(text='\U0001F338', callback_data='color_pink'),
                                                InlineKeyboardButton(text='\U0001F383', callback_data='color_orange'),
                                                InlineKeyboardButton(text='\U0001F34B', callback_data='color_yellow'),
                                                InlineKeyboardButton(text='\U0001F332', callback_data='color_green'),
                                                InlineKeyboardButton(text='\U0001F340', callback_data='color_lightgreen'),
                                                InlineKeyboardButton(text='\U0001F42C', callback_data='color_lightblue'),
                                                InlineKeyboardButton(text='\U0001F4D8', callback_data='color_blue'),
                                                InlineKeyboardButton(text='\U0001F47E', callback_data='color_purple'))