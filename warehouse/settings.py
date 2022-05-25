"""
Django settings for warehouse project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'register.apps.RegisterConfig',
    'library.apps.LibraryConfig',
    'notice.apps.NoticeConfig',
    'information.apps.InformationConfig',
    'django_cleanup.apps.CleanupConfig',
    'overview.apps.OverviewConfig',
    'control.apps.ControlConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'warehouse.middleware.UAmiddleware',
]

ROOT_URLCONF = 'warehouse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'warehouse.context_processors.menu',
                'warehouse.context_processors.version_no',
            ],
            'libraries': {
                'mytag': 'notice.templatetags.mytag',
            },
        },
    },
]

WSGI_APPLICATION = 'warehouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'wh2.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# ------------------------------------------------------------------
# user setting
# ------------------------------------------------------------------
# For Django4
CSRF_TRUSTED_ORIGINS = ['https://*.sophiagardens.org']

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
VERSION_NO = 'Dev.2022-05-23'
MEMBERSHIP_FEE = 270
# ファイルアップロードアプリuploder用
# https://qiita.com/okoppe8/items/86776b8df566a4513e96
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

# アップロードファイルのpermissionとサイズを設定
# https://qiita.com/y-oota/items/8d6d0068abca8e26ab04
# https://docs.djangoproject.com/en/2.2/ref/settings/#file-upload-max-memory-size
# nginxの調整だけでよい.
FILE_UPLOAD_PERMISSIONS = 0o755
# FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

AUTH_USER_MODEL = 'register.User'
NUMBER_GROUPING = 3

LOGIN_URL = 'register:login'
LOGIN_REDIRECT_URL = 'notice:news_card'
LOGOUT_REDIRECT_URL = 'notice:news_card'

# ブラウザを閉じたらログアウトさせる。
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# マークダウンの拡張
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
]

# viewクラスでselectする時のlimit値を設定する。
SELECT_LIMIT_NUM = 100
# コメントを表示する件数。タイトル表示は20個、コメントも20タイトル分表示。
COMMENT_LIMIT = 20

# settings.pyの末尾
try:
    from .private_settings import *
except ImportError:
    pass

try:
    from .local_settings import *
except ImportError:
    pass

# ログ出力先のディレクトリを設定する
LOG_BASE_DIR = os.path.join("logs", )
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    "formatters": {"simple": {"format": "%(asctime)s [%(levelname)s] %(message)s"}},
    # ログの出力方法についての設定。
    "handlers": {
        # DEBUG = Falseの場合、ログファイルに出力する。
        "info": {
            "level": "INFO",
            "filters": ['require_debug_false'],
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 51200,
            "backupCount": 5,
            "filename": os.path.join(LOG_BASE_DIR, "info.log"),
            "formatter": "simple",
        },
        # DEBUG = Falseの場合、ファイル削除時にログファイルに出力する。
        "warning": {
            "level": "WARNING",
            "filters": ['require_debug_false'],
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 51200,
            "backupCount": 5,
            "filename": os.path.join(LOG_BASE_DIR, "warning.log"),
            "formatter": "simple",
        },
        # DEBUG = Trueの場合、コンソールにログ出力する。
        "debug": {
            "level": "DEBUG",
            "filters": ['require_debug_true'],
            "class": 'logging.StreamHandler',
            "formatter": "simple",
        },
    },
    # ロガーはルートロガーのみとする。
    "root": {
        "handlers": ["info", "debug"],
        "level": "INFO",
    },
}

# For debugging
if DEBUG:
    # 開発環境における静的ファイルの場所を指定する。
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )
else:
    # for nginx
    STATIC_ROOT = '/code/static'
