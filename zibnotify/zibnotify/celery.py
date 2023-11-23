import os

from celery import Celery
from .notification import NotificationManager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zibnotify.settings')

app = Celery('zibnotify')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

@app.task(bind=True)
def send_sms(receiver, messege):
    return f"SMS to {receiver}: {messege}"

@app.task(bind=True)
def send_email(receiver, messege):
    return f"Email to {receiver}: {messege}"

@app.task(bind=True)
def send_push_notification(receiver, messege):
    return f"Push Notification to {receiver}: {messege}"


notifier = NotificationManager()
notifier.register('sms', send_sms)
notifier.register('email', send_email)
notifier.register('push_notification', send_push_notification)