#!/usr/bin/env bash

set -e

PROJECT_BASE_PATH='/usr/local/apps/monorbit-api-monolithic'

# echo "thewolfcommander" | echo "Billionaire2201" | read -p 
sudo git pull
# $PROJECT_BASE_PATH/env/bin/python manage.py makemigrations
sudo $PROJECT_BASE_PATH/env/bin/python manage.py migrate
sudo $PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
supervisorctl restart monorbit-api-monolithic

echo "DONE! :)"
