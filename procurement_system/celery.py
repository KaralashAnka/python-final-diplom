import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'procurement_system.settings')

app = Celery('procurement_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'send-daily-reports': {
        'task': 'orders.tasks.send_daily_reports',
        'schedule': crontab(hour=18, minute=0),  # Daily at 6 PM
    },
}
