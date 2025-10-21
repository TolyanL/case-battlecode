#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create a superuser
python manage.py create_superuser

# Start the main process
exec "$@"
