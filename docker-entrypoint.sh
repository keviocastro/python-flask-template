#!/bin/sh
set -e

if [[ $DB_MIGRATE == "true" ]];then
  dockerize -wait tcp://$DB_HOST:$DB_PORT -timeout $DB_WAIT
  flask db upgrade
fi

python ./app.py $API_PORT
