from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()


bot =Bot(token="5974704275:AAENn0SnIZ4iHQj-jdNDbQjoJ5bnFfTSsc8")
dp = Dispatcher(bot, storage=storage)
