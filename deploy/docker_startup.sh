#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Django migrate"
python manage.py migrate --noinput
echo "Run Gunicorn"
gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 starter_app.wsgi:application
