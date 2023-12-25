#!/bin/sh 

echo "excuting entrypoint.sh"

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input 

gunicorn src.wsgi:application --bind 0.0.0.0:8080
