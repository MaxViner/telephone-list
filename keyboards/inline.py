from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os

answ = dict()

bot =Bot(token="5974704275:AAENn0SnIZ4iHQj-jdNDbQjoJ5bnFfTSsc8")
dp = Dispatcher(bot)

urlKb = InlineKeyboardMarkup(row_width=1)
urlBtn1=InlineKeyboardButton(text='link', url='')
urlBtn2=InlineKeyboardButton(text='link', url='')


inbtn = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton(text='Like',callback_data='Like_1'),InlineKeyboardButton(text='no Like',callback_data='Like_-1'))

@dp.message_handler(commands='test')
async def test_com(message:types.Message):
    await message.answer('za vity!',reply_markup=inbtn)

@dp.callback_query_handler(Text(startswith="like_"))
async def www_call(calllback : types.CallbackQuery):
    res =int(calllback.data.split('_')[1])
    if calllback.from_user.id not in answ:
        answ[f'{calllback.from_user.id}']=res
        await calllback.answer("yeah!")
    else:
        await calllback.answer('no', show_alert=True)

executor.start_polling(dp, skip_updates=True)