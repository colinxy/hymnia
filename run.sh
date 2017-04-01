#!/bin/sh

secret_key=$(cat secret_key)
ms_api_key=$(cat ms_api)

env MS_API_KEY="$ms_api_key" SECRET_KEY="$secret_key" PRODUCTION=yes python3 app.py
