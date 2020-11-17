#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $HOST $PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py migrate --noinput
python manage.py collectstatic
gunicorn TP.wsgi:application --bind 0.0.0.0:8000

exec "$@"