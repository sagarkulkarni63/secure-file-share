#!/usr/bin/env bash
set -e
# Run migrations
poetry run python manage.py makemigrations core
poetry run python manage.py migrate
# Start server
exec poetry run python manage.py runserver_plus 0.0.0.0:8000
