#!/bin/sh
cd /app/routejet/
./manage.py createsuperuser --noinput
./manage.py collectstatic --noinput
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata product.json
gunicorn -w 5 routejet.wsgi --timeout=500 -b 0.0.0.0:5000