from aiogram import Router, F, types
from app.config import HELP_CMD, DESCRIPTION, CONNECT_VPN
from app.bot.keyboards import kb1, ikb1, ikb2

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать 👋",
        reply_markup=kb1
    )


@router.message(F.text == "/help")
async def cmd_help(message: types.Message):
    await message.answer(HELP_CMD, parse_mode="HTML")


@router.message(F.text == "/description")
async def cmd_description(message: types.Message):
    await message.answer(DESCRIPTION)


@router.message(F.text == "Подключить VPN")
async def cmd_connect(message: types.Message):
    await message.answer(
        CONNECT_VPN,
        parse_mode="HTML",
        reply_markup=ikb1
    )


# 🔹 Inline callbacks
@router.callback_query(F.data == "wg")
async def choose_wireguard(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Вы выбрали WireGuard.\nВыберите подписку:",
        reply_markup=ikb2
    )
    await callback.answer()


@router.callback_query(F.data == "vless")
async def choose_vless(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Vless временно недоступен 🚧"
    )
    await callback.answer()


@router.message()
async def unknown(message: types.Message):
    await message.answer("❓ Я не понял команду")
