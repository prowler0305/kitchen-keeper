#!/bin/sh
set -e

echo "Running database migrations..."
flask --app run.py db upgrade

echo "Starting Kitchen Keeper"
exec gunicorn -c gunicorn.conf.py "kitchen_keeper:create_app()"