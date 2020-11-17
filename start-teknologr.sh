#!/usr/bin/env bash
# start-teknologr.sh

(python teknologr/manage.py collectstatic -v0 --noinput; touch teknologr/teknologr/wsgi.py) &
(cd teknologr; gunicorn teknologr.wsgi:application --user www-data --bind 0.0.0.0:8010 --workers 3)
