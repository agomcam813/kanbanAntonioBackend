#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL is ready"

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done

echo "Redis is ready"

exec "$@"
