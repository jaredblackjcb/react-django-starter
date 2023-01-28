#!/usr/bin/env bash
# exit on error
set -o errexit

export DJANGO_SETTINGS_MODULE=starter_app.settings_production

echo "Installing python dependencies"
pip install -U pip
pip install -r requirements.txt

echo "Building JS & CSS"
npm install
npm run build

echo "Collecting staticfiles"
python manage.py collectstatic --noinput

echo "Running database migrations"
python manage.py migrate
