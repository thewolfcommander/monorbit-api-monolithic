import datetime
from datetime import timedelta
from decouple import config

import logging
logger = logging.getLogger(__name__)
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', True)

# ALLOWED_HOSTS = ['monorbit-alpha.herokuapp.com', 'localhost', '127.0.0.1', '34.212.227.245']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'corsheaders',
    'django_filters',
    'django_extensions',
    'import_export',
    'rest_framework',

    # Our owned apps
    'accounts',
    'addresses',
    'adminer',
    'cart',
    'core',
    'demo_product',
    'greivances',
    'job_profiles',
    'network',
    'orders',
    'premium',
    'product_catalog',
    'transactions',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'accounts.middlewares.StatsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monorbit.urls'

AUTH_USER_MODEL = 'accounts.User'
IMPORT_EXPORT_USE_TRANSACTIONS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'monorbit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# host = config('SERVER_HOST', True)

# if host:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# else:
    
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('AWS_RDS_DB_NAME', 'AWS_RDS_DB_NAME'),
#         'USER': config('AWS_RDS_USERNAME', 'AWS_RDS_USERNAME'),
#         'PASSWORD': config('AWS_RDS_PASSWORD', 'AWS_RDS_PASSWORD'),
#         'HOST': config('AWS_RDS_HOST', 'AWS_RDS_HOST'),
#         'PORT': 5432,
#     }
# }

# add this below the database configuration
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

REST_FRAMEWORK = {

    'PAGE_SIZE': 20,
    'DATETIME_FORMAT': '%s000',
    'DEFAULT_PAGINATION_CLASS': 'product_catalog.pagination.CustomPageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PARSER_CLASSES': (
       'rest_framework.parsers.JSONParser',
       'rest_framework.parsers.FormParser',
       'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,

}

ATOMIC_REQUESTS = True



"""
S3 Settings for bucket storage
"""
ACCESS_KEY = config('S3_ACCESS_KEY', 'S3_ACCESS_KEY')
SECRET_KEY = config('S3_SECRET_KEY', 'S3_SECRET_KEY')
BUCKET_NAME = config('S3_BUCKET_NAME', 'S3_BUCKET_NAME')


"""
SES Settings for AWS
"""
# EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = config('SES_ACCESS_KEY', 'SES_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = config('SES_SECRET_KEY', 'SES_SECRET_KEY')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = config('SMTP_SERVER', 'SMTP_SERVER')
EMAIL_PORT = config('SMTP_PORT', 'SMTP_PORT')
EMAIL_HOST_USER = config('SMTP_USERNAME', 'SMTP_USERNAME')
EMAIL_HOST_PASSWORD = config('SMTP_PASSWORD', 'SMTP_PASSWORD')



"""
Sentry Setup

Docs : https://docs.sentry.io/platforms/python/django/?_ga=2.983862.60821945.1598358892-1072562326.1598358892
"""

if False:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=config('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate = 1.0,  # It will catch both error and performance. To reduce performance alerts, make it b/w 0 and 1

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
