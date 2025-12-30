from aiogram import Router, F, types
from app.config import HELP_CMD, DESCRIPTION, CONNECT_VPN
from app.bot.keyboards import kb1, ikb1, ikb2

from app.db.database import AsyncSessionLocal
from app.db import crud
from app.vpn.wg_sender import send_wg_to_user

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    """
    /start:
    - проверяем, есть ли пользователь в БД
    - если нет — регистрируем
    - trial НЕ выдаём
    """

    async with AsyncSessionLocal() as session:

        # Проверяем, есть ли пользователь
        user = await crud.get_user_by_tg_id(
            session=session,
            tg_id=message.from_user.id
        )

        # Если новый пользователь — создаём
        if not user:
            await crud.create_user(
                session=session,
                tg_id=message.from_user.id,
                username=message.from_user.username
            )

            text = (
                "👋 Добро пожаловать!\n\n"
                "После выбора VPN-протокола вы получите "
                "пробный период на 3 дня 🎁"
            )
        else:
            text = (
                "👋 С возвращением!\n\n"
                "Вы можете подключить VPN или продлить подписку."
            )

    await message.answer(text, reply_markup=kb1)


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


@router.callback_query(F.data == "wg")
async def choose_wireguard(callback: types.CallbackQuery):
    """
    Пользователь выбрал WireGuard.

    Возможные сценарии:
    1️⃣ Нет подписки → даём trial + выдаём VPN
    2️⃣ Trial активен → выдаём VPN
    3️⃣ Trial закончился → предлагаем оплату
    4️⃣ Платная активна → выдаём VPN
    """

    async with AsyncSessionLocal() as session:

        # Получаем пользователя
        user = await crud.get_user_by_tg_id(
            session=session,
            tg_id=callback.from_user.id
        )

        # Последняя подписка WireGuard
        subscription = await crud.get_latest_subscription(
            session=session,
            user_id=user.id,
            vpn_type="wireguard"
        )

        # ========== СЦЕНАРИЙ 1 ==========
        if subscription is None:
            # 🎁 Создаём trial на 3 дня
            subscription = await crud.create_trial_subscription(
                session=session,
                user_id=user.id,
                vpn_type="wireguard",
                days=3
            )

            text = (
                "🎁 Вам выдан пробный доступ к WireGuard на 3 дня!\n\n"
                "⚙️ Сейчас я подготовлю VPN-конфигурацию."
            )

            # Сообщаем пользователю
            await callback.message.edit_text(text)
            await callback.answer()

            # 🔥 Выдаём WireGuard
            await send_wg_to_user(
                bot=callback.bot,
                chat_id=callback.from_user.id,
            )
            return

        # Проверяем активность подписки
        is_active = crud.is_subscription_active(subscription)

        # ========== СЦЕНАРИИ 2 и 4 ==========
        if is_active:
            remaining_days = (
                subscription.end_date - subscription.start_date
            ).days

            text = (
                "✅ У вас есть активная подписка WireGuard.\n\n"
                f"📅 Действует до: {subscription.end_date.strftime('%d.%m.%Y %H:%M')}\n"
                f"⏳ Осталось дней: {remaining_days}\n\n"
                "⚙️ Подготавливаю VPN-конфигурацию…"
            )

            await callback.message.edit_text(text)
            await callback.answer()

            # 🔥 Выдаём WireGuard (повторно, если нужно)
            await send_wg_to_user(
                bot=callback.bot,
                chat_id=callback.from_user.id,
            )
            return

        # ========== СЦЕНАРИЙ 3 ==========
        text = (
            "⛔ Ваша подписка WireGuard истекла.\n\n"
            "Для продолжения работы VPN выберите тариф 👇"
        )

    # Подписка неактивна → показываем оплату
    await callback.message.edit_text(
        text,
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
