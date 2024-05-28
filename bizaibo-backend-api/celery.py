import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bizaibo-backend-api.settings')

app = Celery('bizaibo-backend-api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
