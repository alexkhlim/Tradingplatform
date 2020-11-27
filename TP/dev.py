import os

from trading_platform.settings import *

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir
)

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "trading_platform",
        "USER": "alex",
        'PASSWORD': '123',
        "HOST": "db",
        "PORT": "5432",
    }
}