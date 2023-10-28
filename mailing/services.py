from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, clients) -> None:
    """
    Функция для оправки писем по почте.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=clients
    )
