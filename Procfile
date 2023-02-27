web: gunicorn config.wsgi
release: python manage.py migrate
worker: celery --app=congregate worker --loglevel=INFO
