#!/bin/bash

# Criar usuário e adicionar ao grupo
useradd -m -g $TORQUE_QUEUE_GROUP $TORQUE_USER || true

# Definir senha do usuário
echo "$TORQUE_USER:$TORQUE_USER_PASS" | chpasswd

trqauthd

celery -A labsoa_website_backend worker --queues=pdf2chemicals_tasks --prefetch-multiplier=1 --autoscale=3,0 --max-tasks-per-child=1 --loglevel=INFO