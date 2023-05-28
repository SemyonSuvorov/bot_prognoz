from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import bot, open_weather_token
from keyboards import client_kb, admin_kb
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
import requests

code_to_smile = {
        "Clear": "Ясно \U0001F505",
        "Clouds": "Облачно \U000026C5",
        "Rain": "Дождь \U0001F327",
        "Drizzle": "Морось \U0001F326",
        "Thunderstorm": "Гроза \U000026C8",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

class FSMClient1(StatesGroup):
    ask_city = State()

class FSMClient2(StatesGroup):
    start = State()
    city = State()
    color = State()

async def command_start(message: types.message):
    if message.text == '/start':
        try:
            await bot.send_message(message.from_user.id,
                                   'Привет! Вы можете получить прогноз одежды либо прогноз погоды, воспользовавшись меню ниже:',
                                   reply_markup=client_kb.welcome_kb)

        except:
            await message.reply('Общение с ботом через лс, напишите ему:\n@cloforecastbot')

async def command_start_callback(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id,
                                   'Привет! Вы можете получить прогноз одежды либо прогноз погоды, воспользовавшись меню ниже:',
                                   reply_markup=client_kb.welcome_kb)
async def weather_choice(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, 'Вы можете отправить название города, либо отправить свою геолокацию:', reply_markup=client_kb.send_loc_kb)

async def get_city(message: types.message):
    await bot.send_message(message.from_user.id, 'Введите название города:')
    await FSMClient1.ask_city.set()


async def city_info(message: types.message, state: FSMContext):
    try:
        await bot.send_message(message.from_user.id, 'Ожидайте...', reply_markup=ReplyKeyboardRemove())
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&"
                         f"units=metric")
        data = r.json()

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        feels_like = data["main"]["feels_like"]
        await message.reply(f"Погода в {city}:\nТемпература: {cur_weather} градусов\nОщущается как: {feels_like} "
                            f"градусов \nВлажность: {humidity} процентов\nСкорость ветра: {wind_speed} м/c\n{wd}", reply_markup=client_kb.cancel_kb)
        async with state.proxy() as info:
            info['weather'] = cur_weather
            info['description'] = weather_description
        await state.finish()
    except:
        await message.reply("\U00002620Проверьте название города\U00002620")


async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    await bot.send_message(message.from_user.id, 'Ожидайте...', reply_markup=ReplyKeyboardRemove())
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&"
            f"units=metric")
        data = r.json()
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        feels_like = data["main"]["feels_like"]
        await bot.send_message(message.from_user.id, f"Погода в {city}:\nТемпература: {cur_weather} градусов\nОщущается как: {feels_like} "
                            f"градусов \nВлажность: {humidity} процентов\nСкорость ветра: {wind_speed} м/c\n{wd}",reply_markup=client_kb.cancel_kb)
    except:
        await message.reply("\U00002620Некорректно отправлена геолокация\U00002620")



###                               ПРОГНОЗ ОДЕЖДЫ                          ####



async def clothes_choice(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, 'Вы можете написать название города, либо отправить свою геолокацию:', reply_markup=client_kb.send_loc_kb)
    await FSMClient2.start.set()

async def clothes_get_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await bot.send_message(message.from_user.id, 'Ожидайте...', reply_markup=ReplyKeyboardRemove())
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&"
            f"units=metric")
        data = r.json()
        weather_description = data["weather"][0]["main"]
        city = data["name"]
        feels_like = data["main"]["feels_like"]
        async with state.proxy() as info:
            info['city'] = city
            info['weather'] = feels_like
            info['description'] = str.lower(weather_description)
        await message.reply('Пожалуйста, выберите желаемый цвет:', reply_markup=admin_kb.colorkb)
        await FSMClient2.color.set()
    except:
        await message.reply("\U00002620Некорректно отправлена геолокация\U00002620")

async def get_city_clothes(message: types.message):
    await bot.send_message(message.from_user.id, 'Введите название города:')
    await FSMClient2.next()   

async def city_info_clothes(message: types.Message, state: FSMContext):
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&"
                         f"units=metric")
        data = r.json()
        weather_description = data["weather"][0]["main"]
        feels_like = data["main"]["feels_like"]
        city = data["name"]
        async with state.proxy() as info:
            info['city'] = city
            info['weather'] = feels_like
            info['description'] = str.lower(weather_description)
        await message.reply('Пожалуйста, выберите желаемый цвет:', reply_markup=admin_kb.colorkb)
        await FSMClient2.next()
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")    

async def get_color_clothes(callback : types.CallbackQuery, state: FSMContext):
    async with state.proxy() as info:
        info['color'] = callback.data.split('_')[1]
        values = tuple(info.values())       
        
        if values[2].title() in code_to_smile:
            wd = code_to_smile[values[2].title()]
        else:
            wd = values[2].title()      
    try:
        await callback.answer()
        await bot.send_photo(callback.from_user.id, await sqlite_db.sql_select(state))
        await bot.send_message(callback.from_user.id,f'Сейчас в {values[0]} температура ощущается как {values[1]} градусов.\n{wd}', reply_markup=client_kb.cancel_kb_clothes)
        await state.finish()
    except:
        await callback.answer()
        await bot.send_message(callback.from_user.id,'К сожалению, не нашлось подхоядщей одежды\U0001F613\nПопробуйте выбрать другой цвет.')
        

async def catcher(message: types.Message):
    await message.reply('Пожалуйста, поспользуйтесь командой на клавиатуре')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])  
    dp.register_callback_query_handler(command_start_callback, Text(equals='cancel'))
    dp.register_callback_query_handler(weather_choice, Text(equals='weather'))
    dp.register_message_handler(get_city, Text(equals='Отправить город'))
    dp.register_message_handler(city_info, state=FSMClient1.ask_city)
    dp.register_message_handler(handle_location, content_types=['location'])
    # ПРОГНОЗ ОДЕЖДЫ
    dp.register_callback_query_handler(clothes_choice, Text(equals='clothes'))
    dp.register_message_handler(get_city_clothes, Text(equals='Отправить город'), state=FSMClient2.start)
    dp.register_message_handler(clothes_get_location, content_types=['location'], state=FSMClient2.start)
    dp.register_message_handler(city_info_clothes, state=FSMClient2.city)
    dp.register_callback_query_handler(get_color_clothes, Text(startswith='color_'), state=FSMClient2.color)
    dp.register_message_handler(catcher)