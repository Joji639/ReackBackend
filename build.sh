#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
email='admin@gmail.com';
password='admin123';

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password
    )
"