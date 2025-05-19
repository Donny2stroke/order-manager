#!/bin/bash

echo "Starting backend initialization..."

# Run migrations
python manage.py migrate

# Create superuser admin if it does not exist
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

# Prompt for seeds
if [ "$RUN_SEED" = "y" ]; then
    echo "Seed execution..."
    python manage.py shell < seed.py
    echo "Imported sample data"
else
    echo "Seeds ignored"
fi

# Start the server
echo "Starting Django..."
exec python manage.py runserver 0.0.0.0:8000
