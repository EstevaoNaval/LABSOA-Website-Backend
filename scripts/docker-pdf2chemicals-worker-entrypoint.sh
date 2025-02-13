#!/bin/bash
set -e

trqauthd

exec gosu ${PDF2CHEMICALS_WORKER_UID}:${DATA_GID} celery -A labsoa_website_backend worker --queues=pdf2chemicals_tasks --prefetch-multiplier=1 --autoscale=3,0 --max-tasks-per-child=1 --loglevel=INFO
