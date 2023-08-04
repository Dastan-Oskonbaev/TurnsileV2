import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_subscriptions': {
        'task': 'apps.payments.tasks.clear_subscriptions',
        'schedule': crontab(hour=0, minute=0),
        'kwargs': {},
    },
    'activate_payment': {
        'task': 'apps.payments.tasks.activate_payment',
        'schedule': crontab(hour=0, minute=0),
        'kwargs': {},
    },
}
