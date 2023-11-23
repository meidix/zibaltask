from .celery import app as celery_app
from .celery import notifier as manager

__all__ = ('celery_app',)