from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'ckeditor',
    'widget_tweaks',
    'admin_notification',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_cleanup.apps.CleanupConfig',
    'django_render_partial',
    'django_social_share',
    'hitcount',
    'jalali_date',
    'django_jalali',
    'rest_framework',
    'colorfield',
    # My Apps
    'apps.home_app.apps.HomeAppConfig',
    'apps.contact_app.apps.ContactAppConfig',
    'apps.product_app.apps.ProductAppConfig',
    'apps.blog_app.apps.BlogAppConfig',
    'apps.account_app.apps.AccountAppConfig',
    'apps.cart_app.apps.CartAppConfig',
    'apps.zarinpal_app.apps.ZarinpalAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Electronic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.context_processors.data_to_base',
            ],
        },
    },
]

WSGI_APPLICATION = 'Electronic.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
SITE_ID = 1

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

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = "account_app.CustomUser"

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ckeditor configsp---------------------------------------
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': 1000,
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.product_app.pagination.CustomPagination',
    'PAGE_SIZE': 100,
}

# Email Configs---------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Admin panel Notification Config----------------------------
NOTIFICATION_MODEL = 'cart_app.UserOrder'

# Zarinpal SETTING--------------------------------------------
RSI_PUBLIC_KEY = os.path.join(BASE_DIR, '0480752990.txt')
MERCHANT = config('ZARINPAL_MERCHANT')
SANDBOX = config('ZARINPAL_SANDBOX', cast=bool, default=False)

# GHASEDAK SETTING---------------------------------------------
KAVENEGAR_APIKEY = config('KAVENEGAR_APIKEY')
KAVENEGAR_OTP_TEMPLATENAME = config('KAVENEGAR_OTP_TEMPLATENAME')
KAVENEGAR_VERIFYORDER_TEMPLATENAME = config('KAVENEGAR_VERIFYORDER_TEMPLATENAME')

# CACHE SYSTEM SETTING-----------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Celery Configuration
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_ENABLE_UTC = True
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
