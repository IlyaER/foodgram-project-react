#!/bin/bash

python manage.py migrate
python manage.py loaddata fixtures/fixtures.json
python manage.py collectstatic --no-input
