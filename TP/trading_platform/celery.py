import os, sys

from celery import Celery

import trading_platform.settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading_platform.settings')

sys.path.append(os.path.abspath('trading_platform'))

app = Celery('trading_platform')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "create_trade": {
        "task": "api.tasks.create_trade",
        "schedule": 30,
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
