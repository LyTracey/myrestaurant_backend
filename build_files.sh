#!/usr/bin/env bash

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files 
python3 manage.py collectstatic