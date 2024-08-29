#!/usr/bin/env sh
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

echo 'Running migrations...'
touch db/db.sqlite3
python manage.py migrate
echo 'Migrated!'

echo 'Starting Exsomnis...'
gunicorn --config gunicorn-cfg.py site_wei.wsgi
