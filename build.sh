#!/usr/bin/env bash
# Exit on error
set -o errexit  

pip install -r requirements.txt  

python manage.py collectstatic --noinput  
python manage.py migrate  

# MEDIA fayllarni staticfiles ichiga ham ko‘chirish
mkdir -p staticfiles/media
cp -r media/* staticfiles/media/ || true
