#!/usr/bin/env bash

# Install dependencies
echo "[INFO] Install dependencies"
pip install --upgrade pip
pip install -r requirements.txt

# Make migrations
echo "[INFO] Apply database migrations"
python3 manage.py makemigrations
python3 manage.py migrate

# Collect static files 
echo "[INFO] Collect static files"
python3 manage.py collectstatic

# Write defualt data to database if preprod branch
if [[ $ENVIRONMENT == "preprod" ]]
then
  echo "[INFO] Writing to database"
  python3 manage.py runscript database_setup
fi
