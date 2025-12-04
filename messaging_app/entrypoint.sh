#!/bin/bash
set -e

echo "Waiting for database..."
python manage.py check --deploy || true

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
