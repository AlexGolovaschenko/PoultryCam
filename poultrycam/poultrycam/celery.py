from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poultrycam.settings')

app = Celery('poultrycam')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'update-photo-list-every-30-minutes': {         # name of the scheduler
        'task'      : 'update_photos_list',         # task name which we have created in tasks.py
        'schedule'  : timedelta(minutes=30),        # set the period of running
    },

    'print-hello-every-10-seconds': {        
        'task'      : 'print_hello',        
        'schedule'  : timedelta(seconds=10),       
    },

}



