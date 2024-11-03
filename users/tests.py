from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Subscription, Payment
from .services import check_payment_status

User = get_user_model()


class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    @patch("stripe.checkout.Session.retrieve")
    def test_payment_status_update(self, mock_stripe_retrieve):
        # Подготовка имитации успешного ответа от Stripe
        mock_stripe_retrieve.return_value = {"payment_status": "paid"}

        # Создаем платеж с session_id
        payment = Payment.objects.create(
            user=self.user, session_id="test_session_id", amount=2000
        )

        # Проверяем функцию check_payment_status
        is_paid = check_payment_status(payment)
        self.assertTrue(is_paid)

        # Проверяем, что подписка обновлена
        subscription, created = Subscription.objects.get_or_create(user=self.user)
        self.assertTrue(subscription.is_subscribed)

        # Проверяем, что подписка уже существует
        self.assertFalse(created)
