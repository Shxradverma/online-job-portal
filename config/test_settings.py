"""SQLite unit/integration settings; production middleware is tested separately."""
from .settings import *
DEBUG = True
SECURE_SSL_REDIRECT = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
MIDDLEWARE = [item for item in MIDDLEWARE if not item.startswith("whitenoise.")]
STORAGES = {
    "default": {"BACKEND":"django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND":"django.contrib.staticfiles.storage.StaticFilesStorage"},
}
MAILERS = {"default":{"BACKEND":"django.core.mail.backends.locmem.EmailBackend"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
