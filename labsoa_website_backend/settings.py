import os
import sys
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_ROOT_DIR = os.getenv("BASE_ROOT_DIR")

API_BASE_URL = os.getenv("API_BASE_URL")

SECRET_KEY = os.getenv('SECRET_KEY')

FRONTEND_URL = os.getenv("FRONTEND_URL")
FRONTEND_EMAIL_CONFIRMATION_ENDPOINT = os.getenv("FRONTEND_EMAIL_CONFIRMATION_ENDPOINT")

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'django-api'
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_EXPOSE_HEADERS = ["content-disposition"]

AUTH_USER_MODEL = 'user.User'

CACHES = {
    "default" : {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = [
    "user.apps.UserConfig",
    "authentication.apps.AuthenticationConfig",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Authentication libs
    "django.contrib.auth",
    "django.contrib.sites",
    "rest_framework",
    "knox",
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_spectacular",
    "django_filters",
    "django_celery_results",
    "django_clamd",
    "import_export",
    "import_export_extensions",
    "chemicals.apps.ChemicalsConfig",
    "pdf2chemicals_service.apps.Pdf2ChemicalsServiceConfig",
    "email_service.apps.EmailServiceConfig"
]



PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware"
]

ROOT_URLCONF = "labsoa_website_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "labsoa_website_backend.wsgi.application"

DATA_DIR = os.getenv('DATA_ROOT_DIR')

MEDIA_RELATIVE_PATH = os.getenv('MEDIA_RELATIVE_PATH')
MEDIA_ROOT = os.path.join(DATA_DIR, MEDIA_RELATIVE_PATH)
MEDIA_URL = os.getenv('MEDIA_URL')

STATIC_RELATIVE_PATH = os.getenv('STATIC_RELATIVE_PATH')
STATIC_ROOT = os.path.join(DATA_DIR, STATIC_RELATIVE_PATH)
STATIC_URL = os.getenv('STATIC_URL')

DATABASES = {
    "default": {
        "ENGINE": os.getenv('DATABASE_ENGINE'),
        "NAME": os.getenv('DATABASE_NAME'),
        "USER": os.getenv('DATABASE_USER'),
        "PASSWORD": os.getenv('DATABASE_PASSWORD'),
        "HOST": os.getenv('DATABASE_HOST'),
        "PORT": os.getenv('DATABASE_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

HEADLESS_ONLY = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication'
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
    'VERSION_PARAMETER': 'version',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}

SITE_ID = 1

ACCOUNT_ADAPTER = "authentication.adapters.CustomAccountAdapter"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
SITES_ENABLED = True

REST_AUTH = {
    "PASSWORD_RESET_USE_SITES_DOMAIN": True,
    'TOKEN_MODEL': None,
    'USE_JWT': False,
    'REGISTER_SERIALIZER': 'authentication.serializer.CustomRegisterSerializer',
}

REST_KNOX = {
    'TOKEN_TTL': timedelta(days=2),
    'AUTO_REFRESH': True,
    'AUTH_HEADER_PREFIX': 'Bearer'
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'LabSOADB API',
    'DESCRIPTION': 'Retrieve our chemicals through this API endpoints',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/',
    'SERVE_PUBLIC': False,
    'EXCLUDE_SCHEMAS': True,
    'POSTPROCESSING_HOOKS': [],
    'EXCLUDE_PATHS': ['/schema/']
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,  # Log para stdout
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

CLAMD_USE_TCP = True
CLAMD_TCP_ADDR = 'clam-container-01'
CLAMD_TCP_SOCKET = 3310
CLAMD_ENABLED = True

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_TIMEZONE = "America/Sao_Paulo"
CELERY_TASK_TRACK_STARTED = True
CELERY_AUTH_TOKEN = os.getenv('CELERY_AUTH_TOKEN')
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'queue_durable': True,
    'message_persistent': True,
    'heartbeat': 600
}
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_DEFAULT_DELIVERY_MODE = 'persistent'
CELERY_WORKER_PREFETCH_MULTIPLIER = 1 

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"