from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from news_portal import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Post)
def news_created(instance, created, **kwargs):
    if not created or instance.type != 'NE':
        return

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
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
