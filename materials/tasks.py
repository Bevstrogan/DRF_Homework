from datetime import datetime, timezone, timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Course, Subscription
from users.models import User


@shared_task
def send_mail(course_id):
    instance = Course.objects.filter(pk=course_id).first()
    if instance:
        subscribers = Subscription.objects.filter(course=instance)
        if len(list(subscribers)) > 0:
            subs = []
            for subscriber in subscribers:
                subs.append(User.objects.get(pk=subscriber.user.pk).email)
            send_mail(
                subject=f'Курс {instance.name} обновлен',
                message=f'Курс {instance.name}, на который вы подписаны обновлен',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=subs
            )

@shared_task
def check_user():
    active_users = User.objects.filter(is_active=True)
    now = datetime.now(timezone.utc)
    for user in active_users:
        if user.last_login:
            if now - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()
                print(f'Аккаунт {user} больше не активен из-за бездействия')