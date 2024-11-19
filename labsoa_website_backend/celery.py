import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labsoa_website_backend.settings')

app = Celery('labsoa_website_backend')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()