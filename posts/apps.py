from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'

    def ready(self):
        from . import signals
