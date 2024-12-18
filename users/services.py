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
    if payment is None:
        return None

    session_id = payment.session_id
    print("Session ID:", session_id)  # Проверка session_id

    if not session_id:
        return False

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        payment_status = session.get("payment_status")
        print("Payment Status:", payment_status)

        if payment_status == "paid":
            # Установление подписки в активное состояние
            subscription, _ = Subscription.objects.get_or_create(user=payment.user)
            subscription.is_subscribed = True
            subscription.save()
            return True
        return False

    except stripe.error.StripeError as e:
        print("Stripe error:", e)
        return False
    except Exception as e:
        print("Unexpected error:", e)
        return False
