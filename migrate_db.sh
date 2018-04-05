#!/bin/bash
echo "\n== MIGRATE =="
python src/manage.py makemigrations austria
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py createcachetable
echo "Database migrated succesfully."
