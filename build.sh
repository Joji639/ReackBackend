#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# 🔥 LOAD DATA (products + users)
python manage.py loaddata data.json || true

# 🔥 CREATE ADMIN (only if not exists)
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
email='admin@gmail.com';
password='admin123';
username='admin';

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        username=username,
        password=password
    )
"