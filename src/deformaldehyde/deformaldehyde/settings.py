"""
Django settings for deformaldehyde project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^&lorcrcacsp^ggh6k+7@&=ep3e@$evai3o$g$jpahb797i#ab'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'example.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'ckeditor',
    'ckeditor_uploader',
    'haystack',
    'fullurl',

    'dashboard',
    'members',
    'comments',
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

ROOT_URLCONF = 'deformaldehyde.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deformaldehyde.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deformaldehyde',
        'USER': 'root',
        'PASSWORD': 'root.123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'members.account'
LOGIN_URL = '/login/'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "comm_static"),
# )

MEDIA_URL = '/media/'
MEDIA_ROOT = (
     os.path.join(BASE_DIR, 'media').replace('\\', '/')
)

## CKEDITOR
CKEDITOR_UPLOAD_PATH = 'ckeditor_images/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'toolbar_YourCustomToolbarConfig': [
        #     {'name': 'basicstyles',
        #      'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript']},
        #     {'name': 'links', 'items': ['Link', 'Unlink']},
        #     {'name': 'insert',
        #      'items': ['CodeSnippet', 'Image', 'Table', 'PageBreak']},
        #     '/',
        #     {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
        # ],
        # 'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'tabSpaces': 4,
        # 'extraPlugins': ','.join([
        #     'uploadimage', # the upload image feature
        #     'div',
        #     'autolink',
        #     'autoembed',
        #     'embedsemantic',
        #     'autogrow',
        #     'widget',
        #     'dialog',
        #     'lineutils',
        #     'codesnippet'
        # ]),
        'width': 'auto',
        'codeSnippet_theme': 'atelier-dune.dark',
    }
}

SITE_ID = 1
BAIDU_NOTIFY_URL = "http://data.zz.baidu.com/urls?site=www.ws6988.com&token=HgVYOxYmTWbQpWwY"
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'deformaldehyde.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    }
}

# 添加此项，当数据库改变时，会自动更新索引，非常方便
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
