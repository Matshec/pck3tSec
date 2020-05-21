#!/bin/sh
printf "Starting django server \n"
python api/manage.py runserver 0.0.0.0:8000 &
printf "Starting application \n"
python runcore.py eth0 || echo "No problemo"
