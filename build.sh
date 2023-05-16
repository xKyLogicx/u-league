#!/bin/bash

# Build the project
echo "Building the project..."
pytho -m pip install -r requirements.txt

echo "Make Migration..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collect Static Files..."
python manage.py collectstatic --noinput
