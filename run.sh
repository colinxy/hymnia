#!/bin/bash

set -e

workers=4
if [ ! -z "$1" ]; then
    workers="$1"
fi

# script has to run in current directory
. envs

TIMEOUT=360                     # 6 mins

gunicorn --bind 0.0.0.0:80 wsgi:app \
         --workers "$workers" --timeout "$TIMEOUT"
