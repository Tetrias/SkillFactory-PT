import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'action_every_day': {
        'task': 'news.tasks.LimitReset',
        'schedule': crontab(hour=0, minute=0),
    },
    'action_every_week': {
        'task': 'news.tasks.WeeklyNewsReport',
        'schedule': crontab(minute=0, hour=8, day_of_week='mon'),
    },
}

app.autodiscover_tasks()
