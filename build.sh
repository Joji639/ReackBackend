#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

echo "🔥 Checking if data exists..."

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.exists():
    print('🔥 No users found → loading data...')
    import subprocess
    subprocess.run(['python', 'manage.py', 'loaddata', 'data.json'])
else:
    print('✅ Data already exists → skipping load')
"