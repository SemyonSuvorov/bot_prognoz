from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot, open_weather_token
from keyboards.client_kb import send_loc_kb
from aiogram.types import ReplyKeyboardRemove
import requests


async def command_start(message: types.message):
    if message.text == '/start':
        try:
            await bot.send_message(message.from_user.id,
                                   'Привет! Вы можете получить прогноз погоды, воспользовавшись меню ниже:',
                                   reply_markup=send_loc_kb)

        except:
            await message.reply('Общение с ботом через лс, напишите ему:\n@cloforecastbot')


async def get_city(message: types.message):
    await message.answer('Введите название города:')


async def city_info(message: types.message):
    code_to_smile = {
        "Clear": "Ясно \U0001F505",
        "Clouds": "Облачно \U000026C5",
        "Rain": "Дождь \U0001F327",
        "Drizzle": "Морось \U0001F326",
        "Thunderstorm": "Гроза \U000026C8",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
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
                            f"градусов \nВлажность: {humidity} процентов\nСкорость ветра: {wind_speed} м/c\n{wd}")
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    code_to_smile = {
        "Clear": "Ясно \U0001F505",
        "Clouds": "Облачно \U000026C5",
        "Rain": "Дождь \U0001F327",
        "Drizzle": "Морось \U0001F326",
        "Thunderstorm": "Гроза \U000026C8",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
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
        await message.reply(f"Погода в {city}:\nТемпература: {cur_weather} градусов\nОщущается как: {feels_like} "
                            f"градусов \nВлажность: {humidity} процентов\nСкорость ветра: {wind_speed} м/c\n{wd}")
    except:
        await message.reply("\U00002620 Некорректно отправлена геолокация \U00002620")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(get_city, Text(equals='Отправить город', ignore_case=True))
    dp.register_message_handler(handle_location, content_types=['location'])
    dp.register_message_handler(city_info)
