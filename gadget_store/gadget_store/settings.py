import os
from pathlib import Path
import dj_database_url

# ----------------------------------------------------------
# BASE & ENVIRONMENT SETTINGS
# ----------------------------------------------------------
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://cyberstore_8101_user:5ZjLGC00uiBSe7zFzVLkpxZ0zygqFgH2@dpg-d0ogf66uk2gs738lnap0-a/cyberstore_8101')

BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key should be stored in an environment variable in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'tgiug7wrfay903ywyr9t94TB*rt8RE8r*er86RT*&IYTBH(&%t7tir^eU^rE&^R8uR&^E5787)')

# DEBUG mode is off by default; enable via env var
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Hosts
ALLOWED_HOSTS = ["*", "cyberstore-n03u.onrender.com"]

# ----------------------------------------------------------
# Applications & Middleware
# ----------------------------------------------------------
INSTALLED_APPS = [
    # Django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    # Custom apps
    'products',
    'cart',
    'orders',
    'users',
]

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gadget_store.urls'

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
                'cart.context_processors.cart_count',
                'cart.context_processors.cart_contents',
                'products.context_processor.categories_processor',
                'products.context_processor.wishlist_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'gadget_store.wsgi.application'

# ----------------------------------------------------------
# Database (PostgreSQL via Render)
# ----------------------------------------------------------
# Render automatically provides DATABASE_URL env var
DATABASE_URL = os.environ.get('DATABASE_URL')

if DEBUG:
    # Use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Use PostgreSQL in production (on Render)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }

# ----------------------------------------------------------
# Password validation
# ----------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# ----------------------------------------------------------
# Internationalization
# ----------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------
# Static & Media files
# ----------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ----------------------------------------------------------
# Security settings for production
# ----------------------------------------------------------
if not DEBUG:
    # Secure SSL/TLS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60  # adjust as needed
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ----------------------------------------------------------
# Default primary key
# ----------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------------------------------------
# Authentication redirects
# ----------------------------------------------------------
LOGIN_URL = 'auth'
LOGIN_REDIRECT_URL = 'home'
