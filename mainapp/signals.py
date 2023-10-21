from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post, PostCategory
from .tasks import mailing_task


@receiver(m2m_changed, sender=PostCategory)
def notify_create_post(sender, instance, action, **kwargs):
    if action == "post_add":
        all_cat = instance.category.all()
        subs_list = [cat.subscribers.all() for cat in all_cat]
        mail_set = set()
        for cat in subs_list:
            for sub in cat:
                mail_set.add(sub.email)

        mailing_task.delay(instance.title, list(mail_set),
                           instance.text, instance.slug)


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
