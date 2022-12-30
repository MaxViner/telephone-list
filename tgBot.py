from createBot import dp
from dp import sqlbase
from aiogram.utils import executor



async def on_startup(_):
    print("бот робит")
    sqlbase.asq_start()
from Handlers import client, others,admin

client.register_handlers_client(dp)
admin.registe_handler_admin(dp)
others.register_handlers_other(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)