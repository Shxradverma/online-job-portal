"""
Django settings for the OnlineJobPortal project.

Configuration is read from environment variables.
"""

import os
from pathlib import Path

import django
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
from django.core.exceptions import ImproperlyConfigured


# ------------------------------------------------------------
# BASE DIRECTORY
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------
# ENVIRONMENT HELPERS
# ------------------------------------------------------------

def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"true", "1", "yes", "on"}


def env_list(name, default=""):
    return [
        item.strip()
        for item in os.environ.get(name, default).split(",")
        if item.strip()
    ]


# ------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")

if not SECRET_KEY.strip():
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY is missing or empty. "
        "Set it in your environment before starting Django."
    )

# Enable explicitly for local development.
DEBUG = env_bool("DEBUG", default=False)

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
)

RENDER_EXTERNAL_HOSTNAME = os.environ.get(
    "RENDER_EXTERNAL_HOSTNAME", ""
).strip()

if (
    RENDER_EXTERNAL_HOSTNAME
    and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS
):
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Origins must include a scheme, for example https://example.com.
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_HTTPONLY = True

# Enable HSTS explicitly after verifying production HTTPS.
SECURE_HSTS_SECONDS = (
    int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
    if not DEBUG
    else 0
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    not DEBUG
    and env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS")
)
SECURE_HSTS_PRELOAD = (
    not DEBUG
    and env_bool("SECURE_HSTS_PRELOAD")
)


# ------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",

    # Project apps
    "accounts",
    "candidates",
    "recruiters",
    "companies",
    "jobs",
    "applications",
    "resumes",
    "notifications",
    "messaging",
    "interviews",
    "analytics",
    "ai_matching",
    "api",
]


# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ------------------------------------------------------------
# URLS AND WSGI
# ------------------------------------------------------------

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SQLITE_PATH", BASE_DIR / "db.sqlite3"),
    },
}


# ------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------

if os.environ.get("DATABASE_URL"):
    import dj_database_url
    DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600, ssl_require=not DEBUG)

# Enable only behind a trusted proxy which overwrites X-Forwarded-Proto.
if env_bool("TRUST_PROXY", default=False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ------------------------------------------------------------
# DJANGO REST FRAMEWORK
# ------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle", "rest_framework.throttling.UserRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"anon": "60/minute", "user": "300/minute", "login": "10/minute"},
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


# ------------------------------------------------------------
# STATIC FILES
# ------------------------------------------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ------------------------------------------------------------
# UPLOADED MEDIA
# ------------------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", BASE_DIR / "media"))


# ------------------------------------------------------------
# EMAIL
# ------------------------------------------------------------

# Local development prints emails to the terminal.
# Production defaults to SMTP.
_mail_backend = os.environ.get(
    "EMAIL_BACKEND",
    (
        "django.core.mail.backends.console.EmailBackend"
        if DEBUG
        else "django.core.mail.backends.smtp.EmailBackend"
    ),
)

_smtp_options = {
    "host": os.environ.get("EMAIL_HOST", "localhost"),
    "port": int(os.environ.get("EMAIL_PORT", "587")),
    "username": os.environ.get("EMAIL_HOST_USER", ""),
    "password": os.environ.get("EMAIL_HOST_PASSWORD", ""),
    "use_tls": env_bool("EMAIL_USE_TLS", default=True),
    "use_ssl": env_bool("EMAIL_USE_SSL", default=False),
    "timeout": int(os.environ.get("EMAIL_TIMEOUT", "30")),
}

if _smtp_options["use_tls"] and _smtp_options["use_ssl"]:
    raise ImproperlyConfigured(
        "EMAIL_USE_TLS and EMAIL_USE_SSL cannot both be enabled."
    )

if django.VERSION >= (6, 1):
    MAILERS = {
        "default": {
            "BACKEND": _mail_backend,
        },
    }

    if _mail_backend == "django.core.mail.backends.smtp.EmailBackend":
        MAILERS["default"]["OPTIONS"] = _smtp_options

else:
    EMAIL_BACKEND = _mail_backend
    EMAIL_HOST = _smtp_options["host"]
    EMAIL_PORT = _smtp_options["port"]
    EMAIL_HOST_USER = _smtp_options["username"]
    EMAIL_HOST_PASSWORD = _smtp_options["password"]
    EMAIL_USE_TLS = _smtp_options["use_tls"]
    EMAIL_USE_SSL = _smtp_options["use_ssl"]
    EMAIL_TIMEOUT = _smtp_options["timeout"]

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "webmaster@localhost",
)


# ------------------------------------------------------------
# DEFAULT PRIMARY KEY
# ------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024
LOGIN_REDIRECT_URL = "/dashboard/"

SIMPLE_JWT = {"CHECK_REVOKE_TOKEN": True}
