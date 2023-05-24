from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from data_base import sqlite_db
from keyboards import admin_kb

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    is_rain = State()
    min_temp = State()
    max_temp = State()
    color = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Вы админ этого бота!", reply_markup=admin_kb.button_case_admin)


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ну ладно :-<')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            await message.photo[-1].download(destination_file=f'shoes/{message.photo[-1].file_id}.jpg')
            with open(f'shoes/{message.photo[-1].file_id}.jpg', 'rb') as picture:
                data['photo'] = picture.read()
                data['file_name'] = f'{message.photo[0].file_id}.jpg'
        await FSMAdmin.next()
        await message.reply('Теперь оцени, насколько твоя обувь устойчива к осадкам (0-10)')


async def load_is_rain(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['is_raining'] = float(message.text)
        await FSMAdmin.next()
        await message.reply('Теперь напиши минимальную комфортную температуру в этой паре')


async def load_min_temp(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['min_temp'] = float(message.text)
        await FSMAdmin.next()
        await message.reply('Теперь напиши максимальную комфортную температуру в этой паре')


async def load_max_temp(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['max_temp'] = float(message.text)
        await FSMAdmin.next()
        await message.reply('Теперь выбери цвет своих кроссовок', reply_markup=admin_kb.colorkb)


async def load_color(callback : types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == ID:
        async with state.proxy() as data:
            data['color'] = callback.data.split('_')[1]
        await callback.answer()
        await sqlite_db.sql_add_command(state)
        await bot.send_message(callback.from_user.id, 'Успешно добавлено!')
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, Text(equals='загрузить', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_is_rain, state=FSMAdmin.is_rain)
    dp.register_message_handler(load_min_temp, state=FSMAdmin.min_temp)
    dp.register_message_handler(load_max_temp, state=FSMAdmin.max_temp)
    dp.register_callback_query_handler(load_color, Text(startswith='color_'), state=FSMAdmin.color)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
