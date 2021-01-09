import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A boolean that turns on/off environment dev mode.
LOCAL = True if os.getenv('DJANGO_SETTINGS_LOCAL', 'False') == 'True' else False

# A boolean that turns on/off debug mode.
# Don't run with debug turned on in production.
DEBUG = True if os.getenv('DJANGO_SETTINGS_DEBUG', 'False') == 'True' else False

# A secret key for this particular Django installation.
# Used in secret-key hashing algorithms.
# Set this in your settings, or Django will complain loudly.
SECRET_KEY = os.getenv('DJANGO_SETTINGS_SECRET_KEY', '')

# Hosts/domain names that are valid for this site.
# "*" matches anything, ".example.com" matches "example.com" and all subdomains.
ALLOWED_HOSTS = os.getenv('DJANGO_SETTINGS_ALLOWED_HOSTS', '').split(',')

# Internationalization.
#   https://docs.djangoproject.com/en/3.1/topics/i18n/
# A string representing the language code for this installation.
# All choices can be found here:
#   http://www.i18nguy.com/unicode/language-identifiers.html.
LANGUAGE_CODE = 'en-us'
# Local time zone for this installation.
# All choices can be found here:
#   https://en.wikipedia.org/wiki/List_of_tz_zones_by_name (although not all systems may support all possibilities).
# When USE_TZ is True, this is interpreted as the default user time zone.
TIME_ZONE = 'UTC'
# A boolean that specifies whether Django’s translation system should be enabled.
# This provides an easy way to turn it off, for performance.
# If this is set to False, Django will make some optimizations so as not to load the translation machinery.
USE_I18N = True
# A boolean that specifies if localized formatting of data will be enabled by default or not.
# If this is set to True, Django will display numbers and dates using the format of the current locale.
USE_L10N = True
# A boolean that specifies if datetimes will be timezone-aware by default or not.
# If this is set to True, Django will use timezone-aware datetimes internally.
# Otherwise, Django will use naive datetimes in local time.
USE_TZ = True

# The Python dotted path to the WSGI application that Django's internal server (runserver) will use.
# If "None", the return value of "django.core.wsgi.get_wsgi_application" is used, thus preserving the same behavior as previous versions of Django.
# Otherwise, this should point to an actual WSGI application object.
WSGI_APPLICATION = 'backend.wsgi.application'

# List of strings representing installed apps.
INSTALLED_APPS = [
    # Django Apps.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-Party Apps.
    'rest_framework',
    'storages',
    # Apps.
    'backend.security.apps.SecurityConfig',
    'backend.dashboard.apps.DashboardConfig',
]

# List of middleware to use.
# Order is important, in the request phase, these middlewares will be applied in the order given and in the response phase the middlewares will be applied in reverse order.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# A string representing the full Python import path to your root URL conf.
ROOT_URLCONF = 'backend.urls'

# Database.
#   https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# A dictionary containing the settings for all databases to be used with Django.
# It is a nested dictionary whose contents map a database alias to a dictionary containing the options for an individual database.
if LOCAL is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DJANGO_SETTINGS_DB_ENGINE', ''),
            'HOST': os.getenv('DJANGO_SETTINGS_DB_HOST', ''),
            'PORT': os.getenv('DJANGO_SETTINGS_DB_PORT', ''),
            'NAME': os.getenv('DJANGO_SETTINGS_DB_NAME', ''),
            'USER': os.getenv('DJANGO_SETTINGS_DB_USER', ''),
            'PASSWORD': os.getenv('DJANGO_SETTINGS_DB_PASSWORD', ''),
        }
    }

# A list containing the settings for all template engines to be used with Django.
# Each item of the list is a dictionary containing the options for an individual engine.
TEMPLATES = [
    {
        # The template backend to use.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Directories where the engine should look for template source files, in search order.
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend', 'templates'),
        ],
        # Whether the engine should look for template source files inside installed applications.
        'APP_DIRS': True,
        # Extra parameters to pass to the template backend.
        # Available parameters vary depending on the template backend.
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

# Static files (CSS, JavaScript, Images).
#   https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'static-files'),
]
if LOCAL is True:
    # Absolute path to the directory static files should be collected to.
    # Example:
    #   "/var/www/example.com/static/".
    STATIC_ROOT = os.path.join(BASE_DIR, 'cdn', 'static-files' + '/')
    # URL that handles the static files served from STATIC_ROOT.
    # Example:
    #   "http://example.com/static/", "http://static.example.com/".
    STATIC_URL = '/static/'

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example:
    #   "/var/www/example.com/media/".
    MEDIA_ROOT = os.path.join(BASE_DIR, 'cdn', 'media-files' + '/')
    # URL that handles the media served from MEDIA_ROOT.
    # Examples:
    #   "http://example.com/media/", "http://media.example.com/". It must end in a slash if set to a non-empty value.
    MEDIA_URL = '/media/'
else:
    # Amazon Web Services Configuration.
    AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_SETTINGS_AWS_STORAGE_BUCKET_NAME', '')
    AWS_ACCESS_KEY_ID = os.getenv('DJANGO_SETTINGS_AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_SETTINGS_AWS_SECRET_ACCESS_KEY', '')
    AWS_S3_CUSTOM_DOMAIN = '{aws_storage_bucket_name}.s3.amazonaws.com'.format(aws_storage_bucket_name=AWS_STORAGE_BUCKET_NAME)

    STATICFILES_LOCATION = 'static-files'
    STATICFILES_STORAGE = 'backend.storages.StaticStorage'
    STATIC_URL = 'https://{aws_s3_custom_domain}/{staticfiles_location}/'.format(aws_s3_custom_domain=AWS_S3_CUSTOM_DOMAIN, staticfiles_location=STATICFILES_LOCATION)

    MEDIAFILES_LOCATION = 'media-files'
    DEFAULT_FILE_STORAGE = 'backend.storages.MediaStorage'
    MEDIA_URL = 'https://{aws_s3_custom_domain}/{mediafiles_location}/'.format(aws_s3_custom_domain=AWS_S3_CUSTOM_DOMAIN, mediafiles_location=MEDIAFILES_LOCATION)

# The custom model as the default user model for the django project.
AUTH_USER_MODEL = 'security.UserModel'
# A list of authentication backend classes (as strings) to use when attempting to authenticate a user.
AUTHENTICATION_BACKENDS = ['backend.security.backends.UserBackend', ]
# Password validation.
#   https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
# Password validation can prevent the use of many types of weak passwords.
# However, the fact that a password passes all the validators does not guarantee that it is a strong password.
# There are many factors that can weaken a password that are not detectable by even the most advanced password validators.
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
# Auth URL.
REGISTER_URL = 'security.dj:authenticate:register'
REGISTER_REDIRECT_URL = 'security.dj:authenticate:login'
LOGIN_URL = 'security.dj:authenticate:login'
LOGIN_REDIRECT_URL = 'security.dj:profile:index'
LOGOUT_URL = 'security.dj:profile:logout'
LOGOUT_REDIRECT_URL = 'index'

# Django REST Framework (DRF).
REST_FRAMEWORK = {
}
