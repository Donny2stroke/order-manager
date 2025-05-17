#!/bin/bash

echo "Starting backend initialization..."

# Esegui le migrazioni
python manage.py migrate

# Crea superuser admin se non esiste
echo "Verify users..."

echo "
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser admin created')

if not User.objects.filter(username='frontend').exists():
    User.objects.create_user('frontend', 'frontend@example.com', 'frontend')
    print('frontend User created')
" | python manage.py shell

# Prompt per i seed
if [ "$RUN_SEED" = "y" ]; then
    echo "Seed execution..."
    python manage.py shell < seed.py
    echo "Imported sample data"
else
    echo "Seeds ignored"
fi

# Avvia il server
echo "Starting Django..."
exec python manage.py runserver 0.0.0.0:8000
