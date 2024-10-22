# Generated by Django 4.2 on 2024-10-18 17:05

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("content", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        help_text="Введите имя или ник",
                        max_length=30,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        help_text="Введите номер телефона",
                        max_length=30,
                        unique=True,
                        verbose_name="Телефон",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "tg_nickname",
                    models.CharField(
                        blank=True,
                        help_text="Введите ник в телеграмме",
                        max_length=50,
                        null=True,
                        verbose_name="Ник в телеграмме",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите аватар",
                        null=True,
                        upload_to="users/avatars/",
                        verbose_name="Аватар",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_date",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        null=True,
                        verbose_name="Дата оплаты",
                    ),
                ),
                (
                    "amount",
                    models.PositiveIntegerField(
                        help_text="Укажите стоимость подписки",
                        verbose_name="Стоимость подписки",
                    ),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("Наличные", "Наличные"),
                            ("Перевод на счет", "Перевод на счет"),
                        ],
                        default="Перевод на счет",
                        max_length=50,
                        verbose_name="Способ оплаты",
                    ),
                ),
                (
                    "session_id",
                    models.CharField(
                        blank=True,
                        help_text="Укажите ID сессии",
                        max_length=250,
                        null=True,
                        verbose_name="ID сессии",
                    ),
                ),
                (
                    "payment_link",
                    models.URLField(
                        blank=True,
                        help_text="Укажите ссылку на оплату",
                        max_length=400,
                        null=True,
                        verbose_name="Ссылка на оплату",
                    ),
                ),
                (
                    "content",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="content.content",
                        verbose_name="Запись",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
    ]
