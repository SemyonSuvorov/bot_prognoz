from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, PollAnswer
from create_bot import bot
from data_base import sqlite_db
from keyboards import admin_kb

ID = None
poll_answer = None

weather_ids = {
    '0': "clear",
    "1": "clouds",
    "2": "rain",
    "3": "drizzle",
    "4": "thunderstorm",
    "5": "snow",
    "6": "mist"
}

class FSMAdmin(StatesGroup):
    photo = State()
    min_temp = State()
    max_temp = State()
    color = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(ID, "Вы админ этого бота!\nВы можете загрусить объект в базу данных, воспользовавшись меню ниже:", reply_markup=admin_kb.button_case_admin)


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await bot.send_message(ID, 'Загрузи фото:')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Загрузка отменена')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            await message.photo[-1].download(destination_file=f'shoes/{message.photo[-1].file_id}.jpg')
            with open(f'shoes/{message.photo[-1].file_id}.jpg', 'rb') as picture:
                data['photo'] = picture.read()
        await bot.send_poll(chat_id=ID, 
                            question="Выбери, под какую погоду подходит данная одежда/обувь:",
                            options=['Ясно \U0001F505', #0
                                     'Облачно \U000026C5', #1
                                     'Дождь \U0001F327', #2
                                     'Морось \U0001F326', #3
                                     'Гроза \U000026C8',#4
                                     'Снег \U0001F328',#5
                                     'Туман \U0001F32B'],#6
                            is_anonymous=False,
                            allows_multiple_answers=True)

async def load_weather(poll: PollAnswer):
    global poll_answer  
    weather_from_poll = str(poll.option_ids)
    poll_answer = [weather_ids[i] for i in weather_from_poll if i in '0123456']
    await FSMAdmin.min_temp.set()
    await bot.send_message(ID, 'Теперь напиши минимальную комфортную температуру в этой одежде/обуви')


async def load_min_temp(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['weather'] = ', '.join(poll_answer)
            data['min_temp'] = float(message.text)
        await FSMAdmin.next()
        await bot.send_message(ID, 'Теперь напиши максимальную комфортную температуру в этой одежде/обуви')


async def load_max_temp(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['max_temp'] = float(message.text)
        await FSMAdmin.next()
        await bot.send_message(ID, 'Теперь выбери цвет одежды/обуви', reply_markup=admin_kb.colorkb)


async def load_color(callback : types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == ID:
        async with state.proxy() as data:
            data['color'] = callback.data.split('_')[1]
        await callback.answer()
        await sqlite_db.sql_add_command(state)
        await bot.send_message(ID, 'Успешно добавлено!',reply_markup=admin_kb.more_or_stop_kb)
        await state.finish()

async def adm_end(callback : types.CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, 'Сеанс модератора завершен')

def register_handlers_admin(dp: Dispatcher):
    dp.register_callback_query_handler(cm_start, Text(equals='Загрузить'))
    dp.register_message_handler(cm_start, Text(equals='загрузить', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_poll_answer_handler(load_weather)
    dp.register_message_handler(load_min_temp, state=FSMAdmin.min_temp)
    dp.register_message_handler(load_max_temp, state=FSMAdmin.max_temp)
    dp.register_callback_query_handler(load_color, Text(startswith='color_'), state=FSMAdmin.color)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(adm_end, Text(equals='stop'))
