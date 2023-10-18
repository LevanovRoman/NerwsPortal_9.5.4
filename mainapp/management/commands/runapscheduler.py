import logging
from datetime import date, timedelta
from ...models import Category
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


def send_period_post(name, email, posts):
    html_content = render_to_string(
        'mainapp/message_send_period_post.html',
        {
            'name': name,
            'posts': posts,
            'link': f'{settings.ALLOWED_HOSTS[1]}/news',
        }
    )
    msg = EmailMultiAlternatives(
        subject="New posts for you for last week",
        from_email=settings.EMAIL_HOST_USER,
        to=[email, ],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def my_job():
    cat_all = Category.objects.all()
    for cat in cat_all:
        start_date = date.today()
        end_date = start_date - timedelta(days=6)
        posts = cat.cats.filter(time_created__range=[end_date, start_date])
        if posts:
            user_data = cat.subscribers.all()
            list_user_data = [(i.username, i.email) for i in user_data]
            for name, email in list_user_data:
                send_period_post(name, email, posts)


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")