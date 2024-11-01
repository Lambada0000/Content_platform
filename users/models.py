from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

payment_choices = (
    ("Наличные", "Наличные"),
    ("Перевод на счет", "Перевод на счет"),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=30, verbose_name="Имя", help_text="Введите имя или ник"
    )
    phone_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    email = models.EmailField(unique=False, verbose_name="Email", blank=True, null=True)
    tg_nickname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Ник в телеграмме",
        help_text="Введите ник в телеграмме",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    subscription = models.OneToOneField('Subscription', null=True, blank=True, on_delete=models.SET_NULL, related_name='user_subscription')

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.phone_number


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription_user')
    date_subscribed = models.DateField(auto_now_add=True)
    is_subscribed = models.BooleanField(default=False)
    subscription_price = models.PositiveIntegerField(
        default=2000,
        help_text="Стоимость подписки в рублях"
    )

    def __str__(self):
        return f"{self.user} подписан."


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="пользователь",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    payment_date = models.DateTimeField(
        default=now, verbose_name="Дата оплаты", blank=True, null=True
    )
    content = models.ForeignKey(
        "content.Content",
        verbose_name="Запись",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    amount = models.PositiveIntegerField(verbose_name="Стоимость подписки", help_text="Укажите стоимость подписки"
                                         )
    payment_type = models.CharField(
        max_length=50,
        verbose_name="Способ оплаты",
        default="Перевод на счет",
        choices=payment_choices,
    )
    session_id = models.CharField(
        max_length=250,
        verbose_name="ID сессии",
        blank=True,
        null=True,
        help_text="Укажите ID сессии",
    )
    payment_link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.amount
