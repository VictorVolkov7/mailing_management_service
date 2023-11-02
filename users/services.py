from django.conf import settings
from django.core.mail import send_mail


def send_email(activation_url, user_email):
    send_mail(
        subject='Подтвердите свой электронный адрес',
        message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: '
                f'http://127.0.0.1:8000/{activation_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )