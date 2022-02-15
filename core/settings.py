from pathlib import Path

import environ

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    DEBUG=(bool, False),
    SECRET_KEY=(str, "33p=mm5j9@ptu1mopm2gd-o4xjs#(n_75b_x(-5r0#6espl2&d"),
    SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, False),
    SECURE_HSTS_PRELOAD=(bool, False),
    SECURE_HSTS_SECONDS=(int, 0),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
)

environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS: list[str] = ["*"]  # env("ALLOWED_HOSTS")

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.admindocs",
    # Third Party App
    "crispy_forms",
    "crispy_tailwind",
    "rest_framework",
    # Local
    "core",
    "acronyms",
    "api",
]

X_FRAME_OPTIONS = "DENY"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    STATIC_URL = "/static/"

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

STATIC_ROOT = Path(BASE_DIR / "static")

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"


LOGIN_REDIRECT_URL = "pages:home"
LOGOUT_REDIRECT_URL = "pages:home"

ADMINS = [("Ryan Cheley", "rcheley@gmail.com")]

SERVER_EMAIL = "rcheley@gmail.com"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}


CURRENCIES = ("USD",)
CURRENCY_CHOICES = [
    ("USD", "USD $"),
]

TEMPLATE_LOADERS = ("django.template.loaders.app_directories.get_app_template_dirs",)

# Security Settings Below

SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS")
SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE")
SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}

SITE_ID = 1

# django-csp settings; you will need to add your URLs below for all versions (PROD, UAT, etc)

csp_list = [
    "'self",
    "'self data:",
    "https://fonts.googleapis.com",
    "https://use.fontawesome.com",
    "https://slackbot.ryancheley.com",
    "http://127.0.0.1:8000",
    "http://www.bohemiancoding.com",
    "http://www.w3.org",
    "'unsafe-eval'",
    "'unsafe-inline'",
    "https://unpkg.com/htmx.org@1.1.0",
    "https://cdn.tailwindcss.com/",
]

CSP_DEFAULT_SRC = csp_list
CSP_SCRIPT_SRC = csp_list
CSP_STYLE_SRC = csp_list + ["'unsafe-inline'"]
CSP_MEDIA_SRC = csp_list
CSP_FONT_SRC = csp_list
CSP_IMG_SRC = csp_list


# Django Feature Policy Settings


PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


SLACK_VERIFICATION_TOKEN = env("SLACK_VERIFICATION_TOKEN")
SLACK_BOT_USER_TOKEN = env("SLACK_BOT_USER_TOKEN")

CONFLUENCE_LINK = env("CONFLUENCE_LINK")
