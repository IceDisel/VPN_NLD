from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb1b1 = KeyboardButton(text='Подключить VPN')
kb1b2 = KeyboardButton(text='/help')
kb1b3 = KeyboardButton(text='/description')

kb1 = ReplyKeyboardMarkup(keyboard=[[kb1b1], [kb1b2, kb1b3]], resize_keyboard=True)

# Инлайн кнопки выбора протокола VPN
kb_1 = InlineKeyboardBuilder()

kb_1.button(text="WireGuard", callback_data="wg")
kb_1.button(text="Vless", callback_data="vless")

kb_1.adjust(2)  # 2 кнопки в каждой строке

ikb1 = kb_1.as_markup()

# Инлайн кнопки выбора оплаты
kb_2 = InlineKeyboardBuilder()

kb_2.button(text="1 мес - 100 руб", callback_data="sub_1")
kb_2.button(text="2 мес - 200 руб", callback_data="sub_2")
kb_2.button(text="3 мес - 300 руб", callback_data="sub_3")
kb_2.button(text="4 мес - 400 руб", callback_data="sub_4")
kb_2.button(text="5 мес - 500 руб", callback_data="sub_5")
kb_2.button(text="6 мес - 600 руб", callback_data="sub_6")

kb_2.adjust(2)  # 2 кнопки в каждой строке

ikb2 = kb_2.as_markup()
