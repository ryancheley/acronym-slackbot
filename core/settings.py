from pathlib import Path

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    DEBUG=(bool, False),
    DATABASE_URL=(str, "psql://postgres:postgres@127.0.0.1:5432/github_actions"),
    SECRET_KEY=(str, "33p=mm5j9@ptu1mopm2gd-o4xjs#(n_75b_x(-5r0#6espl2&d"),
    SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, False),
    SECURE_HSTS_PRELOAD=(bool, False),
    SECURE_HSTS_SECONDS=(int, 0),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
    SLACK_VERIFICATION_TOKEN=(str, ""),
    SLACK_BOT_USER_TOKEN=(str, ""),
    CONFLUENCE_LINK=(str, ""),
    SECURE_PROXY_SSL_HEADER=(str, None),
)

# Read .env file from project root
environ.Env.read_env(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS")

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
    "rest_framework",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    # Local
    "core",
    "acronyms",
    "api",
]

X_FRAME_OPTIONS = "DENY"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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
        "django_model_info.apps.DjangoModelInfoConfig",
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

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR.parent / "db.sqlite3",
#     }
# }
DATABASES = {
    "default": env.db(),
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


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

STATIC_ROOT = Path(BASE_DIR / "static")

# Only include STATICFILES_DIRS if the directory exists (development)
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / "staticfiles",
    ]
else:
    # WhiteNoise configuration for production
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_REDIRECT_URL = "pages:home"
LOGOUT_REDIRECT_URL = "pages:home"

ADMINS = ["rcheley@gmail.com"]

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

# Trust proxy headers from Coolify/Caddy
if proxy_header := env("SECURE_PROXY_SSL_HEADER"):
    header, value = proxy_header.split(",")
    SECURE_PROXY_SSL_HEADER = (header, value)

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
    "https://uat.slackbot.ryancheley.com",
    "https://hetzner.slackbot.ryancheley.com",
    "http://127.0.0.1:8000",
    "https://a753-47-158-193-137.ngrok.io",
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

REST_FRAMEWORK = {"TEST_REQUEST_DEFAULT_FORMAT": "json"}
