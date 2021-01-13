#!/bin/ash
# start-teknologr.sh
echo $MIGRATE

if [ "$MIGRATE" == "True" ]; then
	echo "Performing migration"
	python teknologr/manage.py migrate
fi
python teknologr/manage.py collectstatic -v0 --noinput
touch teknologr/teknologr/wsgi.py
cd teknologr
gunicorn teknologr.wsgi:application --user www-data --bind 0.0.0.0:8010 --workers 3
