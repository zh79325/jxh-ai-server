#!/bin/bash -x

python manage.py runserver 0.0.0.0:8000 --noinput || exit 1
exec "$@"
