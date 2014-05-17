"""
Django settings for cliques project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Determine which environment we're running in.
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    ENV = 'appengine'
elif os.getenv('SETTINGS_MODE') == 'prod':
    ENV = 'localprod'
elif os.getenv('TRAVIS') == 'True':
    ENV = 'travis'
else:
    ENV = 'local'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4wd(bfk2m5qj2k0p7(w6)(q$+o040_+_9y$z^_h%ua^(=v2lb2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'cliques.context_processor.settings_context',
    'cliques.context_processor.polls',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'invite_only',
    'chat_server',
    'poll',
    'notify',
    'website',
]


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)
CORS_ORIGIN_ALLOW_ALL = True

if ENV in ['localprod', 'local']:
    INSTALLED_APPS += [
        'south',
        # 'debug_toolbar',
        # 'appengine_toolkit'
    ]
    # DEBUG_TOOLBAR_PATCH_SETTINGS = False
    # MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.'
    #                        'DebugToolbarMiddleware',)


ROOT_URLCONF = 'cliques.urls'

WSGI_APPLICATION = 'cliques.wsgi.application'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if ENV == 'appengine':
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/cliquesio:main',
            'NAME': 'cliques',
            'USER': 'root',
        }
    }
    MAIL_PROVIDER = 'APPENGINE'
    EMAIL_SENDER = 'josh@slashertraxx.com'
    EMAIL_BACKEND = 'cliques.mail.EmailBackend'
elif ENV == 'localprod':
    # Running in development, but want to access the Google Cloud SQL instance
    # in production.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.environ.get('APPENGINE_IP'),
            'NAME': os.environ.get('APPENGINE_NAME'),
            'USER': os.environ.get('APPENGINE_USERNAME'),
            'PASSWORD': os.environ.get('APPENGINE_PASSWORD')
        }
    }
    MAIL_PROVIDER = 'APPENGINE'
    EMAIL_SENDER = 'josh@slashertraxx.com'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # EMAIL_BACKEND = 'djangoappengine.mail.EmailBackend'
elif ENV == 'travis':
    # Running in development, so use a local MySQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'cliques',
            'USER': 'travis',
        }
    }
    MAIL_PROVIDER = 'DJANGO'
    EMAIL_SENDER = 'josh@slashertraxx.com'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Running in development, so use a local MySQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'cliques',
            'USER': 'root',
            'PASSWORD': 'password',
        }
    }
    MAIL_PROVIDER = 'DJANGO'
    EMAIL_SENDER = 'josh@slashertraxx.com'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # EMAIL_BACKEND = 'djangoappengine.mail.EmailBackend'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_FILE_STORAGE = 'appengine_toolkit.storage.GoogleCloudStorage'
MEDIA_ROOT = 'media'

# AllAuth
AUTH_USER_MODEL = 'website.UserProfile'

ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ADAPTER = 'invite_only.adapter.InviteOnlyAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': 'debug.log',
        # },
    },
    'loggers': {
        'django.request': {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

APPENGINE_TOOLKIT = {
    'APP_YAML': os.path.join(BASE_DIR, 'app.yaml'),
    'BUCKET_NAME': 'cliquesio',
}

SITE_NAME = 'Slashertraxx'

# API
# REST_FRAMEWORK = {
#     # Use hyperlinked styles by default.
#     # Only used if the `serializer_class` attribute is not set on a view.
#     'DEFAULT_MODEL_SERIALIZER_CLASS':
#         'rest_framework.serializers.HyperlinkedModelSerializer',
#
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

# Mime Types
MIME_IMAGES = [
    'image/gif',
    'image/jpeg',
    'image/pjpeg',
    'image/png',
    'image/svg+xml',
    'image/example'
]

MIME_AUDIO = [
    'audio/mpeg',
    'audio/mp4',
    'audio/ogg',
    'audio/vorbis',
    'audio/webm'
]

MIME_VIDEO = [
    'video/mpeg',
    'video/mp4',
    'video/webm',
    'video/x-matroska',
    'video/x-ms-wmv',
    'video/x-flv',
    'video/avi'
]
