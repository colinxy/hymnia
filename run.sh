#!/bin/sh

secret_key=$(cat secret_key)

env SECRET_KEY="$secret_key" PRODUCTION=yes python3 app.py
