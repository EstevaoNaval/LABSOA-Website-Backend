#!/bin/bash
# Aplicar as migrações já criadas
echo "Apply database migrations"
python manage.py migrate --noinput || exit 1

# Criar o site frontend, se necessário
echo "Running create_frontend_site"
python manage.py create_frontend_site

# Iniciar o servidor
echo "Starting server"
exec python manage.py runserver 0.0.0.0:8000
