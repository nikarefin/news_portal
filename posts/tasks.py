from celery import shared_task
from news_portal import settings
from django.contrib.auth.models import User
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
import datetime


@shared_task
def notify_about_news(instance_id):
    instance = Post.objects.get(id=instance_id)
    emails = User.objects.filter(
        subscriber__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Добавлена новость в категории «{instance.category}»'

    text_content = (
        f'{instance.title}\n'
        f'{settings.SITE_URL}{instance.get_absolute_url()}'
    )
    html_content = (
        f'{instance.title}<br>'
        f'<a href="{settings.SITE_URL}{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def notify_about_last_news():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    news = Post.objects.filter(date_joined__gte=last_week, type='NE').order_by('-date_joined')
    categories = set(news.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscriber__user__email', flat=True))
    text_content = '\n'.join([f'{new.title}\n{settings.SITE_URL}/posts/{new.pk}\n' for new in news])
    msg = EmailMultiAlternatives(
        subject='Новости за неделю',
        body=text_content,
        from_email=None,
        to=subscribers,
    )
    msg.attach_alternative(text_content, "text/html")
    msg.send()
