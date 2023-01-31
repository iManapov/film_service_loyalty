#!/bin/sh

python manage.py collectstatic --no-input --clear
python manage.py migrate

uwsgi --strict --ini uwsgi.ini

exec "$@"