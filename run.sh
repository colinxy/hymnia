#!/bin/sh

set -e

workers=4
if [ ! -z "$1" ]; then
    workers="$1"
fi

source envs

gunicorn --bind 0.0.0.0:80 wsgi:app -w "$workers"
