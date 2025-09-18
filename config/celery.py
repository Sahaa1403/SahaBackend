import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
app.conf.broker_url = "redis://default:2bA0TquxVq3mYDJjugPIRwwr@lhotse.liara.cloud:31643/0"
app.conf.result_backend = app.conf.broker_url
