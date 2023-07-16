#!/bin/sh

until nc -z -v -w30 rabbit 5672; do
    echo "Ожидание брокера..."
    sleep 1
  done
  echo "Брокер готов"

exec "$@"