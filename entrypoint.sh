#!/bin/sh

if [ ! -f .env ]; then
  echo ".env file not found. Please create the .env file."
  exec /bin/sh
else
  exec python src/main.py
fi