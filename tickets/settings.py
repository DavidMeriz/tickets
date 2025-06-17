# -*- coding: utf-8 -*-
import os
import sys
import socket
import types

# ---------------------------------------------------------------------------
#  Work-around para Python 3.13+ (el módulo «cgi» se retira del stdlib)
# ---------------------------------------------------------------------------
try:
    import cgi        # pragma: no cover
except ImportError:
    sys.modules['cgi'] = types.ModuleType('cgi')

# ---------------------------------------------------------------------------
#  Rutas base
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ---------------------------------------------------------------------------
#  Seguridad
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-change-me")

# PRO / DEV toggle
if socket.gethostname() == os.environ.get("DJANGO_PRODUCTION_DOMAIN", "localhost"):
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE   = True
else:
    DEBUG = True
    ALLOWED_HOSTS = []

# ---------------------------------------------------------------------------
#  Aplicaciones instaladas
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'crispy_forms',
    'crispy_bootstrap5',           

    # Apps del proyecto
    'main',
]

# ---------------------------------------------------------------------------
#  Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tickets.urls'
WSGI_APPLICATION = 'tickets.wsgi.application'

# ---------------------------------------------------------------------------
#  Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------------------------------------------------------------------
#  Base de datos
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# ---------------------------------------------------------------------------
#  Internacionalización
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE     = 'Europe/Madrid'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

# ---------------------------------------------------------------------------
#  Archivos estáticos y de medios
# ---------------------------------------------------------------------------
STATIC_URL  = '/static/'
STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT",
                             os.path.join(BASE_DIR, 'static_root'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL  = '/media/'
MEDIA_ROOT = os.environ.get("DJANGO_MEDIA_ROOT",
                            os.path.join(BASE_DIR, 'media'))

# ---------------------------------------------------------------------------
#  Autenticación
# ---------------------------------------------------------------------------
LOGIN_REDIRECT_URL = '/inbox/'
LOGIN_URL          = '/'

# ---------------------------------------------------------------------------
#  Crispy-Forms
# ---------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK         = "bootstrap5"

# ---------------------------------------------------------------------------
#  Django 3.2+: clave primaria por defecto
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
#  Email y Admins
# ---------------------------------------------------------------------------
ADMINS = [(os.environ.get("DJANGO_ADMIN_NAME", "admin"),
           os.environ.get("DJANGO_ADMIN_EMAIL", "admin@example.com"))]
MANAGERS = ADMINS

EMAIL_HOST          = os.environ.get("DJANGO_EMAIL_HOST", "localhost")
EMAIL_HOST_USER     = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")

# ---------------------------------------------------------------------------
#  Logging
# ---------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'simple':  {'format': '%(levelname)s %(message)s'},
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class':  'logging.FileHandler',
            'filename': os.environ.get("DJANGO_LOG_FILE",
                                       os.path.join(BASE_DIR, 'django.log')),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class':  'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django':          {'handlers': ['file'],        'level': 'INFO',  'propagate': True},
        'django.request':  {'handlers': ['mail_admins'], 'level': 'ERROR', 'propagate': False},
        'main':            {'handlers': ['file'],        'level': 'INFO'},
    },
}
