#!/bin/sh

# Очікуємо доступність бази даних
python event_management/wait_for_db.py

# Застосовуємо міграції
cd event_management
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Запускаємо сервер
exec "$@" 