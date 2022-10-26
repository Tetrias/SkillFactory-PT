import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adBoard.settings')

app = Celery('adBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'action_every_week': {
        'task': 'ad.tasks.WeeklyNewsReport',
        'schedule': crontab(minute=0, hour=0, day_of_week='mon'),
    },
}

app.autodiscover_tasks()
