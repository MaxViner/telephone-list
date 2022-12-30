from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove

b1=KeyboardButton('/поиск_по_имени')
b2=KeyboardButton('/поиск_по_номеру')
b3=KeyboardButton('/поиск_контакта')
b4=KeyboardButton('поделиться',request_contact=True)
b5=KeyboardButton('/лист_контактов')
b6=KeyboardButton('/полный_просмотр')
b7=KeyboardButton('/краткий_просмотр')

kb_klient = ReplyKeyboardMarkup(resize_keyboard=True)
wiev_kb = ReplyKeyboardMarkup(resize_keyboard=True)

button_MORE = KeyboardButton('more')
kb_klient.add(b1,b2).row(b4,b3).add(b5)
wiev_kb.add(b6).add(b7)