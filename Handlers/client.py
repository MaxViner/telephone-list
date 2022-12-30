import time

from aiogram import types,Dispatcher
from createBot import bot, dp
from keyboards import kb_klient, wiev_kb
from aiogram.types import ReplyKeyboardRemove
from dp import sqlbase
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

n, ret=0, 0
dict={}
last=False
one_more, no_more=True, False

class FSMclient(StatesGroup):
    search_name = State()
    search_lastname=State()
    waiting=State()


# @dp.message_handler(commands=['start','help'])
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<НАЧАЛО РАБОТЫ>>>>>>>>>>>>>>>>>>>>>>>>>
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,"hi boyes", reply_markup=kb_klient)
        await message.delete()
        print("+")

    except:
        await message.reply("пиши боту эээээээ")



# @dp.message_handler(commands=['найти по имени'])
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<ПРОСМОТРЕ КОНТАКТОВ ПО ИМЕНАМ>>>>>>>>>>>>>>>>>>>>>>>>>
async def search_phone_command(message:types.Message):
    global dict,n
    await bot.send_message(message.from_user.id,'info')
    print("+")
    read = await sqlbase.sql_reader()
    print(read)
    print(len(read))
    for ret in range(n,len(read)) :
        dict[ret] = read[ret]
        n+=1
        await bot.send_message(message.from_user.id,text="________________",
                                       reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f"{ret+1} {read[ret][1]} {read[ret][2]}\n",
                                                                                                                          callback_data=f'vis {ret}')))
        n=0

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<ПРОСМОТРЕ КОНТАКТОВ ПО НОМЕРУ>>>>>>>>>>>>>>>>>>>>>>>>>

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('vis '))
async def get_number(callback_query :types.CallbackQuery):

    global one_more, n, dict
    print(callback_query.data)
    for ret in range(len(dict)):
        if str(ret)==callback_query.data.replace("vis ",''):
            print(dict.get(ret))
            await callback_query.answer( dict.get(ret)[3],show_alert=True)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('vis '))
async def get_name(callback_query: types.CallbackQuery):

    global one_more, n, dict
    print(callback_query.data)
    for ret in range(len(dict)):
        if str(ret) == callback_query.data.replace("vis ", ''):
            print(dict.get(ret))
            await callback_query.answer((dict.get(ret)[1]+dict.get(ret)[2]), show_alert=True)


    # await bot.send_photo(message.from_user.id, read[ret][0], f"{read[ret][1]} {read[ret][2]}\n - {read[ret][-1]}\n - {read[ret][-2]}")

async def search_name_command(message: types.Message):
    global one_more, no_more, dict
    global n
    print("+")
    read = await sqlbase.sql_reader()
    print(read)
    print(len(read))
    for ret in range(n, len(read)):
        dict[ret] = read[ret]
        await bot.send_message(message.from_user.id, text="________________",
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f"  {read[ret][3]}\n",
                                                            callback_data=f'name {ret}')))




@dp.callback_query_handler(lambda x: x.data and x.data.startswith('name '))
async def get_name(callback_query: types.CallbackQuery):

    global one_more, n, dict
    print(callback_query.data)
    for ret in range(len(dict)):
        if str(ret) == callback_query.data.replace("name ", ''):
            print(dict.get(ret))
            await callback_query.answer(dict.get(ret)[1]+dict.get(ret)[2], show_alert=True)

    @dp.callback_query_handler(lambda x: x.data and x.data.startswith('name '))
    async def get_name(callback_query: types.CallbackQuery):

        global one_more, n, dict
        print(callback_query.data)
        for ret in range(len(dict)):
            if str(ret) == callback_query.data.replace("vis ", ''):
                print(dict.get(ret))
                await callback_query.answer((dict.get(ret)[1] + dict.get(ret)[2]), show_alert=True)





# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<ПОИСК ПО ИМЕНИ>>>>>>>>>>>>>>>>>>>>>>>>>

async def search_command(message:types.Message):
    await FSMclient.search_name.set()
    await message.answer('введи имя')

async def search_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMclient.next()

    read = await sqlbase.sql_search(data['name'],None,False)
    print(data['name'])
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]} {ret[2]}\n - {ret[-1]}"
                                                           f"\n - {ret[-2]}")

    await message.reply('фамилия?')


async def search_last_name(message: types.Message, state: FSMContext):
    global last
    last=True
    async with state.proxy() as data:
        data['last_name'] = message.text

    await state.finish()
    read = await sqlbase.sql_search(data['name'],data['last_name'], True)
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]} {ret[2]}\n - {ret[-1]}"
                                                           f"\n - {ret[-2]}")
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<ПРОСМОТР КОНТАКТОВ>>>>>>>>>>>>>>>>>>>>>>>>>
async def wiev(message: types.Message):
    await bot.send_message(message.from_user.id, 'полный или краткий просмотр?', reply_markup=wiev_kb)
    await message.delete()

async def all_wiev(message: types.Message):
    print("+")
    global one_more,n
    await bot.send_message(message.from_user.id,"список контактов:", reply_markup=kb_klient)
    read = await sqlbase.sql_reader()
    print(read)
    while n<len(read):

                await bot.send_photo(message.from_user.id, read[n][0], f"{read[n][1]} {read[n][2]}\n - {read[n][-1]}"
                                                               f"\n - {read[n][-2]}")
                n += 1
                print(n)
    n=0


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<КРАТКИЙ ПРОСМОТР КОНТАКТОВ>>>>>>>>>>>>>>>>>>>>>>>>>
async def short_wiev(message: types.Message):
    read=await sqlbase.sql_reader()
    await bot.send_message(message.from_user.id,"лискт контактов :" ,reply_markup=kb_klient)
    for ret in read:
        await bot.send_message(message.from_user.id, f"{ret[1]} {ret[2]}\n - {ret[3]}")




def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(search_phone_command,commands=['поиск_по_имени'])
    dp.register_message_handler(wiev , commands=['лист_контактов'])
    dp.register_message_handler(search_name_command, commands=['поиск_по_номеру'])
    dp.register_message_handler(search_command,commands=['поиск_контакта'])
    dp.register_message_handler(search_name,state=FSMclient.search_name)
    dp.register_message_handler(search_last_name, state=FSMclient.search_lastname)
    dp.register_message_handler(all_wiev, commands=['полный_просмотр'])
    dp.register_message_handler(short_wiev, commands=['краткий_просмотр'])