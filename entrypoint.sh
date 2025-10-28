#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create a superuser
python manage.py create_superuser

# Create default badges
python manage.py create_badges

# Create user groups
python manage.py create_user_groups

# Collect static files
python manage.py collectstatic --no-input --clear

# Start the main process
exec "$@"
