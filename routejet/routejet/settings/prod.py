from .base import *  # pylint: disable=E0402 W0401

ADMINS = [
    x.split(':') for x in env.list('DJANGO_ADMINS')  # pylint: disable=E0602
]

ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),  # pylint: disable=E0602
        'USER': env('POSTGRES_USER'),  # pylint: disable=E0602
        'PASSWORD': env('POSTGRES_PASSWORD'),  # pylint: disable=E0602
        'HOST': env('POSTGRES_HOST'),  # pylint: disable=E0602
        'PORT': 5432,
    }
}

# ALLOWED_ORIGINS = [
#     f'https://{os.environ.get("RENDER_EXTERNAL_HOSTNAME")}'  # pylint: disable=E0602
# ]
ALLOWED_ORIGINS = ['*']
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS.copy()
