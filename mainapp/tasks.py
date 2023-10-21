from datetime import date, timedelta
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from celery import shared_task
import time

from .models import Category
from django.conf import settings


@shared_task
def mailing_task(title, mail_set, text, slug):
    subject = f'Новый пост: {title}'
    html_content = render_to_string(
        'mainapp/message_create_post.html',
        {
            'title': title,
            'text': text,
            'link': f'{settings.ALLOWED_HOSTS[1]}/news/{slug}/',
        }
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body=title,
        from_email=settings.EMAIL_HOST_USER,
        to=mail_set,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


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


@shared_task
def mailing_on_monday():
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


