import sqlite3
from createBot import bot

def asq_start():
    global base, cur
    base = sqlite3.connect("db.db")
    cur = base.cursor()

    if base:
        print("db robit")
    # base.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT ,name TEXT PRIMARY KEY ,descr TEXT ,price TEXT)")
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO storage VALUES (?, ?, ?, ?, ?)", tuple(data.values()))
        base.commit()
        print('saving')

async def sql_view(message):
    print("жж")
    for ret in cur.execute("SELECT * FROM storage").fetchall():
        await bot.send_photo(message.from_user.id,ret[0],f"{ret[1]} {ret[2]}\n - {ret[-1]}\n - {ret[-2]}")

async def sql_reader():
    return cur.execute("SELECT * FROM storage").fetchall()

async def sql_del(data):
    cur.execute("DELETE FROM storage WHERE name == ?", (data,))
    base.commit()

async def sql_search(data_n, data_ln, last):
    if last:
        print("тру")
        return cur.execute("SELECT * FROM storage WHERE name == ? AND last_name == ?",
                           (data_n,data_ln,)).fetchall()
    return cur.execute("SELECT * FROM storage WHERE name == ?", (data_n,)).fetchall()






    # async with state.proxy() as data:
    #      await message.reply(str(data))