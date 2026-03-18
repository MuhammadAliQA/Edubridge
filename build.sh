#!/usr/bin/env bash
set -o errexit

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collect static..."
python manage.py collectstatic --no-input

echo "Migrate..."
python manage.py migrate --noinput