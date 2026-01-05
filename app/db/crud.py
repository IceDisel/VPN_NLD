from datetime import datetime, timedelta

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, Subscription


# =========================
# Работа с пользователями
# =========================

async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
    """
    Получить пользователя по Telegram ID.
    Вернёт объект User или None.
    """
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, tg_id: int, username: str | None) -> User:
    """
    Создаёт нового пользователя в БД.
    """
    user = User(tg_id=tg_id, username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


# =========================
# Работа с подписками
# =========================

async def has_trial(session: AsyncSession, user_id: int, vpn_type: str) -> bool:
    """
    Проверяет, был ли у пользователя trial
    для конкретного vpn_type (например wireguard).
    """
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id, Subscription.vpn_type == vpn_type,
                                   Subscription.is_trial.is_(True)))
    return result.scalar_one_or_none() is not None


async def create_trial_subscription(session: AsyncSession, user_id: int, vpn_type: str, days: int = 3) -> Subscription:
    """
    Создаёт trial-подписку на N дней.
    """
    now = datetime.utcnow()

    sub = Subscription(
        user_id=user_id,
        vpn_type=vpn_type,
        is_trial=True,
        is_active=True,
        start_date=now,
        end_date=now + timedelta(days=days)
    )

    session.add(sub)
    await session.commit()
    await session.refresh(sub)
    return sub


async def get_latest_subscription(session, user_id: int, vpn_type: str) -> Subscription | None:
    """
    Возвращает ПОСЛЕДНЮЮ подписку пользователя
    для конкретного vpn_type.

    Почему последнюю:
    - подписки могут продлеваться
    - нас интересует актуальная
    """
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id, Subscription.vpn_type == vpn_type)
        .order_by(desc(Subscription.end_date)).limit(1))

    return result.scalar_one_or_none()


def is_subscription_active(subscription: Subscription) -> bool:
    """
    Проверяет, активна ли подписка по времени.

    ❗ НЕ доверяем is_active слепо,
    а сравниваем даты.
    """
    now = datetime.utcnow()
    return subscription.end_date > now


async def attach_wg_to_subscription(session, subscription_id: int, public_key: str, ip: str, ):
    """
    Сохраняет WireGuard-данные в подписке.
    """
    result = await session.execute(select(Subscription).where(Subscription.id == subscription_id))
    sub = result.scalar_one()

    sub.wg_public_key = public_key
    sub.wg_ip = ip

    await session.commit()


async def create_paid_subscription(session, user_id: int, vpn_type: str, days: int, ):
    """
    Создаёт платную подписку на N дней
    """

    now = datetime.utcnow()

    sub = Subscription(
        user_id=user_id,
        vpn_type=vpn_type,
        is_trial=False,
        is_active=True,
        start_date=now,
        end_date=now + timedelta(days=days),
    )

    session.add(sub)
    await session.commit()
    return sub
