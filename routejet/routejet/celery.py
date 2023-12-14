import os
import ssl
from celery import Celery

module_settings = os.environ.get('DJANGO_SETTINGS_MODULE')

if module_settings == 'routejet.settings.local':
    app = Celery('routejet')
else:
    app = Celery(
        'routejet',
        broker_use_ssl={
            'ssl_cert_reqs': ssl.CERT_NONE
        },
        redis_backend_use_ssl={
            'ssl_cert_reqs': ssl.CERT_NONE
        }
    )

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
