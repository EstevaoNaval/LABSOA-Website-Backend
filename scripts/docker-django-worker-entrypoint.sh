#!/bin/bash
celery -A labsoa_website_backend worker --queues=django_tasks --prefetch-multiplier=1 --autoscale=1,0 --loglevel=INFO