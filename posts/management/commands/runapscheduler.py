import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from posts.models import Post, Category

logger = logging.getLogger(__name__)


def notify_about_new_articles():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=1)
    articles = Post.objects.filter(date_joined__gte=last_week, type='AR').order_by('-date_joined')
    categories = set(articles.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscriber__user__email', flat=True))
    text_content = '\n'.join([f'{article.title}\n{settings.SITE_URL}/posts/{article.pk}\n' for article in articles])
    msg = EmailMultiAlternatives(
        subject='Новые статьи за неделю',
        body=text_content,
        from_email=None,
        to=subscribers,
    )
    msg.attach_alternative(text_content, "text/html")
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            notify_about_new_articles,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            id="notify_about_new_articles",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'notify_about_new_articles'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
