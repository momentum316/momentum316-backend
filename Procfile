web: gunicorn config.wsgi
release: python manage.py migrate
worker: celery --app=config worker --loglevel=INFO
