#!/bin/sh
set -e

echo "Waiting for MySQL..."

# Wait for MySQL using Python
python - <<END
import time
import sys
from sqlalchemy import create_engine
import os

db_uri = os.environ.get("DB_URI")
if not db_uri:
    print("DB_URI not set")
    sys.exit(1)

engine = create_engine(db_uri)

while True:
    try:
        conn = engine.connect()
        conn.close()
        break
    except Exception:
        time.sleep(1)
END

echo "MySQL is up, running migrations..."

# Flask migrations
flask db init 2>/dev/null || true
flask db migrate -m "auto migration"
flask db upgrade

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:5000 wsgi:app
