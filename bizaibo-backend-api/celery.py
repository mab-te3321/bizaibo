import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bizaibo-backend-api.settings')

app = Celery('bizaibo-backend-api')
app.conf.update(
    broker_url='sqla+sqlite:///celerydb.sqlite',
    result_backend='db+sqlite:///results.sqlite',
    beat_scheduler='celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler',
    beat_schedule_filename='celery_schedule.db',
)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')