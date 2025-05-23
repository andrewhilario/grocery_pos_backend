"""
Django settings for grocery_pos_backend project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x96#$a0+tlcm_@4j-lp%o1ys%8ro)mnzf2!wfsl7()6jsffgsm"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "users",
    "products",
    "api",
    "procurement",
    "sales",
    "suppliers",
    "corsheaders",
    "drf_spectacular"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "grocery_pos_backend.urls"

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

WSGI_APPLICATION = "grocery_pos_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": tmpPostgres.path.replace("/", ""),
        "USER": tmpPostgres.username,
        "PASSWORD": tmpPostgres.password,
        "HOST": tmpPostgres.hostname,
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


AUTH_USER_MODEL = "users.User"

SPECTACULAR_SETTINGS = {
    'TITLE': 'Grocery POS API',
    'DESCRIPTION': 'A REST API for a Grocery Point-of-Sale (POS) System.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'AUTHENTICATION_SCHEMES': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    },
    'SECURITY': [{'Bearer': []}],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'PREPROCESSING_HOOKS': ['grocery_pos_backend.utils.schema_hooks.auto_tag_by_urlprefix'],
    'TAGS': [
        {'name': 'Products', 'description': 'Manage grocery items and inventory.'},
        {'name': 'Orders', 'description': 'Handle sales and transactions.'},
        {'name': 'Customers', 'description': 'Manage customer data.'},
        {'name': 'Auth', 'description': 'User authentication and JWT tokens.'},
    ],
}

USE_DEPRECATED_PYTZ = False


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# For development (optional)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOW_ALL_ORIGINS = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}