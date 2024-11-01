import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price():
    """Создает цену в Stripe """
    price = stripe.Price.create(
        currency="rub",
        unit_amount=200000,
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
