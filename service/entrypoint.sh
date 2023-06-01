#!/bin/sh
set -e
set -x

# Chown the mounted data volume
chown -R service:service "/data/"
chown -R service:service "/service/"
# Launch our service as user 'service'
# exec su -s /bin/sh -c 'PYTHONUNBUFFERED=1 flask --app server run --host=0.0.0.0' service

# Launch our service as user 'service' using Gunicorn with the configuration file
exec su -s /bin/sh -c 'gunicorn --config gunicorn.conf.py server:app'