"""
Django settings for ecommerce project.
"""


from dotenv import load_dotenv

from pathlib import Path

load_dotenv()


# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent


# Security
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-m82iqj#@s*)qnezbrwt+tq2f_e7=ei23hyz^n^st^r%a$q2)bt"
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    ".vercel.app",
    "localhost",
    "127.0.0.1"
]


# Applications

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store',
]


# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise for static files on Vercel
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'ecommerce.urls'


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # If you have project-level templates folder add:
        # BASE_DIR / "templates"
        'DIRS': [
    BASE_DIR / "templates"
],
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'store.context_processors.cart_count',

            ],
        },
    },
]


WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database

import os
import dj_database_url


# Database Configuration

# Database Configuration

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password Validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Language

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# WhiteNoise compression

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)



# Media files

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / "media"



# Default primary key

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'