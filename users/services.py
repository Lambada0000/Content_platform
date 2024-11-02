import stripe
from django.conf import settings
from config.settings import STRIPE_API_KEY
from users.models import Subscription

stripe.api_key = STRIPE_API_KEY


def create_stripe_price():
    """Создает цену в Stripe, используя настройку стоимости подписки"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=settings.SUBSCRIPTION_PRICE * 100,
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


def check_payment_status(payment):
    """Проверяет, оплатил ли пользователь подписку"""
    session_id = payment.payment_id
    print(session_id)
    if not session_id:
        return False

    session = stripe.checkout.Session.retrieve(session_id)
    payment_status = session.get("payment_status")
    print(payment_status)

    if payment_status == "paid":
        # Установление подписки в активное состояние
        subscription, _ = Subscription.objects.get_or_create(user=payment.user)
        subscription.is_subscribed = True
        subscription.save()
        return True
    return False
