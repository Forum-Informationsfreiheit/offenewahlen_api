#!/bin/sh
cd src/
python3 manage.py compilemessages
python3 manage.py collectstatic --no-input
