from .base import *  # pylint: disable=E0402 W0401

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # pylint: disable=E0602
    }
}
