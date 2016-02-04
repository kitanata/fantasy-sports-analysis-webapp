import environ

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env('.env')

SITE_ROOT = root()
site_base = root.path('ackarma/')

STATIC_ROOT = root('staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = root('media')
MEDIA_URL = '/media/'

DEBUG = env('DEBUG')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = (
    site_base('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.EmailUser'

INSTALLED_APPS = (
    'overextends',
    'django_gulp',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.contrib.wagtailstyleguide',
    'wagtailmodeladmin',

    'modelcluster',
    'compressor',
    'taggit',

    'django_nose',
    'debug_toolbar',
    'crispy_forms',

    'home',
    'blog',
    'accounts',
    'subscriptions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    'wagtailmodeladmin.middleware.ModelAdminMiddleware',
)

ROOT_URLCONF = 'ackarma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            site_base('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ackarma.context_processors.global_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'ackarma.wsgi.application'

DATABASES = {
    'default': env.db()
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=.',
]

LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/dashboard'

WAGTAIL_SITE_NAME = 'AC Karma Sports'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

RECURLY_SUBDOMAIN = env('RECURLY_SUBDOMAIN')
RECURLY_API_KEY = env('RECURLY_API_KEY')
RECURLY_SUCCESS_URL = env('RECURLY_SUCCESS_URL')
RECURLY_CANCEL_URL = env('RECURLY_CANCEL_URL')
RECURLY_PUBLIC_KEY = env('RECURLY_PUBLIC_KEY')

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = env('MAILGUN_ACCESS_KEY')
MAILGUN_SERVER_NAME = env('MAILGUN_SERVER_NAME')

COMPRESS_OFFLINE = True
