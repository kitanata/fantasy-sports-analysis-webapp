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

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.EmailUser'

INSTALLED_APPS = (
    'django_gulp',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'crispy_forms',

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ackarma.wsgi.application'

DATABASES = {
    'default': env.db()
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_REDIRECT_URL = '/dashboard'

GRAPPELLI_ADMIN_TITLE = 'AC Karma Sports'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

RECURLY_SUBDOMAIN = env('RECURLY_SUBDOMAIN')
RECURLY_API_KEY = env('RECURLY_API_KEY')
