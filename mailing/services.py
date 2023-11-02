from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog


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


def get_cached_blogs():
    if settings.CACHE_ENABLE:
        key = 'blog_list'
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.order_by('published_date')[:3]
            cache.set(key, blog_list)
    else:
        blog_list = Blog.objects.order_by('published_date')[:3]

    return blog_list
