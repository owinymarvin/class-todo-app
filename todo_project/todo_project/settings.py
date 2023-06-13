from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@_wmow(8vrm_jbb)jc1$mlf!e!s79bhep%%$3^icf(lzj6)16d'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'todo_app',
    'django_crontab',
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

ROOT_URLCONF = 'todo_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'todo_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# timezone was changed to local timezone
TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


"""
    This shows how the email settings in this project where set and the purpose of each setting

    EMAIL_BACKEND: indicates the SMTP backend. 
                    Allows sending emails using the Simple Mail Transfer Protocol (SMTP).

    EMAIL_HOST: shows that the email server is hosted on gmail


    EMAIL_PORT: The port is used to establish connection with the email server. 
                For the Gmail SMTP server, the common port is 587

    EMAIL_HOST_USER: The email address used to send emails.

    EMAIL_HOST_PASSWORD: The "App password" (from gmail). Doesn't use your login password.

    EMAIL_USE_TLS: specifies whether to use Transport Layer Security (TLS) encryption when establishing the connection.

"""


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # We shall change the *console with smtp when we begin hosting  
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'equipstreams@gmail.com'
EMAIL_HOST_PASSWORD = 'kkijtqnllcusuuip'
EMAIL_USE_TLS = True



"""
    The app has 2 cron jobs, 
    1. checks if a task is due in 30 min
    2. checks if a tasks due_datetime has passed by more than 7 days (its overdue)

    cron jobs can be set to run after any interval of time using stars(*).
        '* * * * *'         => min(0-59),hour(0-23),dayOfMonth(1-31),month(1-12),dayOfWeek(0-7)
        '5 * * * *',        => will run 5min past every hour
        '*/5 * * * *',      => will run every 5min

    we have set our cron jobs to run every minute. 

    NB: its important to note that it will only run on a Linux environment as it has dependencies e.g. cron installed. 
        for windows environments, we need a task scheduler.

"""

CRONJOBS = [
    ('* * * * *', 'todo_app.cron.check_if_task_due_30_min'),
    ('* * * * *', 'todo_app.cron.check_if_task_past_7_days'),

]


