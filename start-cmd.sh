#!/bin/sh
# Backend Dockerfile start command.

# Run migrations.
python manage.py db upgrade

# Run gunicorn.
gunicorn -b 0.0.0.0 --workers 2 --log-level DEBUG --timeout 90 manage:app
