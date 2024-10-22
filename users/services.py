import stripe

from config.settings import STRIPE_API_KEY
from content.models import Content

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(content: Content):
    """Создает цену в Stripe на основе контента"""
    subscription_price = content.subscription_price
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(subscription_price * 100),
        product_data={"name": "Подписка"},
    )
    return price


def create_stripe_session(price):
    """Создает сессию оплаты в Stripe"""
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price.get("id"),
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://localhost:8000/",
        cancel_url="http://localhost:8000/",
    )
    return session.get("id"), session.get("url")


def check_payment_status(user):
    """Проверяет, оплатил ли пользователь подписку"""
    session_id = user.payment_id
    print(session_id)
    if not session_id:
        return False

    session = stripe.checkout.Session.retrieve(session_id)
    payment_status = session.get("payment_status")
    print(payment_status)
    if payment_status == "paid":
        return True
    return False
