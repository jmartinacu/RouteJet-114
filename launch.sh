#!/bin/sh
cd /app/routejet/
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser --noinput
./manage.py collectstatic --noinput
./manage.py loaddata product.json
gunicorn -w 5 routejet.wsgi --timeout=500 