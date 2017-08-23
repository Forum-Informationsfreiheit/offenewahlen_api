#!/bin/bash
python src/manage.py makemigrations viz
python src/manage.py makemigrations
python src/manage.py migrate
echo "Database migrated succesfully."