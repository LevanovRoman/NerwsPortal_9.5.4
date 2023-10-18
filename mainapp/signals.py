from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def notify_create_post(sender, instance, **kwargs):
    all_cat = instance.category.all()
    subs_list = [cat.subscribers.all() for cat in all_cat]
    mail_set = set()
    for cat in subs_list:
        for sub in cat:
            mail_set.add(sub.email)
    subject = f'{instance.category} {instance.title}'
    html_content = render_to_string(
        'mainapp/message_create_post.html',
        {
            'title': instance.title,
            'text': instance.text,
            'link': f'{settings.ALLOWED_HOSTS[1]}/news/{instance.slug}/',
        }
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.title,
        from_email=settings.EMAIL_HOST_USER,
        to=mail_set,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(user_signed_up)
def welcome_new_user(sender, **kwargs):
    user = kwargs['user']
    html_content = render_to_string(
        'mainapp/welcome_new_user.html',
        {
            'user': user.username, }
    )
    msg = EmailMultiAlternatives(
        subject='Welcome!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email, ],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

