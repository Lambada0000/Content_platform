from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import Subscription
from content.models import Content


@shared_task
def start_mailshot(content_id):
    """Отправляет сообщения пользователям с подпиской о новом контенте."""
    # Получаем контент по ID
    content = Content.objects.get(id=content_id)

    # Получаем всех пользователей, подписанных на этот контент
    subscriptions = Subscription.objects.filter(content=content, is_subscribed=True)

    # Отправляем письмо каждому подписчику
    for subscription in subscriptions:
        user_email = subscription.user.email
        if user_email:
            send_mail(
                subject="Новое обновление контента!",
                message=f'Новый контент "{content.title}" доступен. Проверьте обновления на платформе!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
            )
    print("start_mailshot: TRUE")
