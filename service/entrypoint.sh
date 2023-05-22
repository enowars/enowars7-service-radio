#!/bin/sh
set -e
set -x

# Chown the mounted data volume
chown -R service:service "/data/"

# Launch our service as user 'service'
exec su -s /bin/sh -c 'PYTHONUNBUFFERED=1 flask --app server run --host=0.0.0.0' service