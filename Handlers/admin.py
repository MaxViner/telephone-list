from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from createBot import dp, bot
from dp import sqlbase
from keyboards import adminKb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    last_name = State()
    number = State()
    descr = State()

# @dp.message_handler(commands=['boss'], is_chat_admin = True)
async def make_changes_command(message:types.Message):
    global ID
    ID= message.from_user.id
    await bot.send_message(message.from_user.id, 'hi there',reply_markup=adminKb.button_case_admin)
    await message.delete()



#
# @dp.message_hendler(commands = 'добавить',state = None)
async def cm_start(message:types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo.set()
        await message.reply('загрузи фото')

# @dp.message_hendler(content_types = ['photo'], state = FSMadmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('введите имя')

# @dp.message_hendler(content_types = ['photo'], state = FSMadmin.photo)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply('фамилия')

#
# @dp.message_hendler(state=FSMadmin.name)
async def load_lastname(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['last_name'] = message.text
        await FSMadmin.next()
        await message.reply('номер')

# @dp.message_hendler(state=FSMadmin.description)
async def load_discr(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['dnumber'] = message.text
        await FSMadmin.next()
        await message.reply('комментарий')

# @dp.message_hendler(state=FSMadmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['descr'] =message.text
        await FSMadmin.next()

        # async with state.proxy() as data:
        #     await message.reply(str(data))

        await sqlbase.sql_add_command(state)
        await state.finish()

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_run(callback_query :types.CallbackQuery):
    await sqlbase.sql_del(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} deleted.', show_alert=True )

@dp.message_handler(commands='удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlbase.sql_reader()
        for ret in read:
            await bot.send_photo(message.from_user.id,ret[0],f"{ret[1]} {ret[2]}\n - {ret[-1]}")
            await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup()
                                   .add(InlineKeyboardButton(f'удалить {ret[1]}',callback_data=f'del {ret[1]}')))



def registe_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['загрузить'],state=None)
    dp.register_message_handler(load_photo, content_types=['photo'],state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_lastname, state=FSMadmin.last_name)
    dp.register_message_handler(load_discr, state=FSMadmin.number)
    dp.register_message_handler(load_price, state=FSMadmin.descr)
    dp.register_message_handler(make_changes_command, commands=['boss'], is_chat_admin = True)