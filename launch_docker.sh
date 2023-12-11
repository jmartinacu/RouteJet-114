#!/bin/sh
cd /routejet/routejet/
./manage.py createsuperuser --noinput
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata product.json
./manage.py runserver 0.0.0.0:8000