from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import notify_about_news


@receiver(post_save, sender=Post)
def news_created(instance, created, **kwargs):
    if not created or instance.type != 'NE':
        return
    notify_about_news(instance.id)
