#!/usr/bin/env bash

# Install dependencies
echo "[INFO] Install dependencies"
pip install --upgrade pip
pip install -r requirements.txt

# Make migrations
echo "[INFO] Apply database migrations - must be done separately"
python3 manage.py makemigrations user_app
python3 manage.py migrate
python3 manage.py makemigrations myrestaurant_app
python3 manage.py migrate

# Collect static files 
echo "[INFO] Collect static files"
python3 manage.py collectstatic

# Create superuser account
echo "[INFO] Creating superuser"
python3 manage.py createsuperuser --noinput
