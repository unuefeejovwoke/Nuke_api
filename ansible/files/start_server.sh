#!/bin/bash

cd /home/ubuntu/app/app
python3 -m venv venv
source venv/bin/activate

venv/bin/pip install --no-cache-dir -r requirements.txt --require-virtualenv
mkdir static
rm staticfiles/staticfiles.json

venv/bin/python manage.py migrate

venv/bin/python manage.py collectstatic --no-input
sudo venv/bin/python manage.py runserver  0.0.0.0:8000 &
# venv/bin/gunicorn django_project.wsgi:application --bind 0.0.0.0:8000 
