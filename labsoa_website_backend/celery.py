import os
import logging
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labsoa_website_backend.settings')

app = Celery('labsoa_website_backend')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()

# Configurar o logging para Celery
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('celery')

@app.task(bind=True)
def debug_task(self):
    logger.info(f'Request: {self.request!r}')