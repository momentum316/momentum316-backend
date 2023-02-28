from __future__ import absolute_import
import os, ssl
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# app = Celery(
#     "myproj",
#     broker_use_ssl={
#         'ssl_cert_reqs': ssl.CERT_NONE
#     },
#     redis_backend_use_ssl={
#         'ssl_cert_reqs': ssl.CERT_NONE
#     }
# )

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
