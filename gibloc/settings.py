import os

# Django settings for gibloc project.

DEBUG = True
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gibloc',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'admin',
        'PASSWORD': 'gibloc',
        'HOST': 'jaba.gib.loc',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES"
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['www.gib.loc','127.0.0.1',]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

#
LOGIN_URL='/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = os.path.join('static').replace('\\','/')
#STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join('static').replace('\\','/'),
    #os.path.join(os.path.dirname(__file__),'static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r&-=p20m7t3m4o)8*os%v$4g9z55fv9*92o+vt=y=so-%0(&hy'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
##     'django.template.loaders.eggs.Loader',
#)

#TEMPLATE_
#CONTEXT_PROCESSORS = (
#  'django.contrib.auth.context_processors.auth',
#  'django.core.context_processors.request',
#)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gibloc.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'gibloc.wsgi.application'

#TEMPLATE_DIRS = (
#    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#    # Always use forward slashes, even on Windows.
#    # Don't forget to use absolute paths, not relative paths.
#    os.path.join('templates').replace('\\','/'),
#    #os.path.join(os.path.dirname(__file__),'templates').replace('\\','/'),
#)

TEMPLATES=[
  {
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[os.path.join('templates').replace('\\','/'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
        # list if you haven't customized them:
        'django.contrib.auth.context_processors.auth',
        #'django.core.context_processors.request',
        'django.template.context_processors.debug',
        'django.template.context_processors.i18n',
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'django.template.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  }
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'squid',
    'squidguard',
    'licenses',
    'tasker',
    'certs',
    'mail',
    'hashez',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(levelname)s : %(message)s',
            'datefmt': '%Y/%b/%d %H/%M/%S'
        },
        'verbose': {
            'format': '%(asctime)s - %(levelname)s in %(module)s:%(filename)s:%(funcName)s at %(lineno)s : %(message)s',
            'datefmt': '%Y/%b/%d %H/%M/%S'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'licenses_info': {
            'level': 'INFO',
            'filename': 'info.log',
            'class': 'logging.FileHandler',
            'formatter': 'simple'
        },
         'debug': {
            'level': 'DEBUG',
            'filename': 'debug.log',
            'class': 'logging.FileHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'licenses': {
            'handlers': ['licenses_info','debug'],
            'level': 'DEBUG'
        }
    }
}

# Added by myself

#AUTH_USER_MODEL=auth.User

SMTP_HOST='10.0.1.120'
SMTP_PORT='25'
SMTP_LOGIN=''
SMTP_PASSWD=''

#DATE_INPUT_FORMATS=('%d/%m/%Y','%d.%m.%Y',)
DATE_INPUT_FORMATS=('%d/%m/%Y',)

TEST_RUNNER='django.test.runner.DiscoverRunner'
