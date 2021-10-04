import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Miners.settings')

app = Celery('Miners')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add_new_stats_every_5_minute': {
        'task': 'statistic.tasks.add_new_stats',
        'schedule': crontab(minute='*/5'),
    }
}
