#!/bin/sh
set -e
set -x

# Chown the mounted data volume
chown -R service:service "/data/"
chown -R service:service "/service/"
# Launch our service as user 'service'
# exec su -s /bin/sh -c 'PYTHONUNBUFFERED=1 flask --app server run --host=0.0.0.0' service

# Launch our service as user 'service' using Gunicorn with the configuration file
cleaner () {
    CLEANUP_DIR=$1;
    echo "Starting cleaner function"
    sleep 1800 #30min
    echo "Cleaner function will now regularly clean"
    while true; do
        cd $CLEANUP_DIR
        find -type f -mmin +30 -delete
        sleep 60
    done
}
DATA_DIR="/service/UPLOAD_FOLDER"
mkdir -p $DATA_DIR
chown -R service:service $DATA_DIR
exec su -s /bin/sh -c 'gunicorn --config gunicorn.conf.py server:app' &
# Launch our service as user 'service' using Gunicorn with the configuration file
cleaner "$DATA_DIR"
