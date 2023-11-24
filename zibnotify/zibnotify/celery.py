import os

from celery import Celery
from .notification import NotificationManager, SMSNotification, EmailNotification, PushNotification

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zibnotify.settings')

app = Celery('zibnotify')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

@app.task(bind=True, queue='notification_queue', max_retries=5)
def send_sms(self, notif):
    try:
        sms = SMSNotification.from_dict(notif)
        return f"via SMS: {str(sms)}"
    except:
        self.retry()

@app.task(bind=True, queue='notification_queue', max_retries=5)
def send_email(self, notif):
    try:
        mail = EmailNotification.from_dict(notif)
        return f"via Email: {str(mail)}"
    except:
        self.retry()

@app.task(bind=True, queue='notification_queue', max_retries=5)
def send_push_notification(self, notif):
    try:
        pn = PushNotification.from_dict(notif)
        return f"Via Push Notification : {str(pn)}"
    except:
        self.retry()


notifier = NotificationManager('mongodb://zibal:pass123Sec@db:27017', 'zibal_db', 'celery_tasks')
notifier.register('sms', send_sms)
notifier.register('email', send_email)
notifier.register('push_notification', send_push_notification)