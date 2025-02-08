from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()
KEY = os.getenv('KEY')
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = KEY
JWT_SECRET = KEY
DEBUG = os.getenv("DEBUG") == "True"
SITE_ID = 2
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ACCOUNT_EMAIL_VERIFICATION = "none"
AUTH_USER_MODEL = "accounts.User"
#APPEND_SLASH = True




if os.getenv("STAGE") == "PRODUCTION":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": "lhotse.liara.cloud",
            "PORT": 30645,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }



# APP CONFIGURATION
DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.sites",
)
THIRD_PARTY_APPS = (
    "rest_framework",
    "django_filters",
    "corsheaders",
    "gunicorn",
    "whitenoise",
    "ckeditor",
    "ckeditor_uploader",
    "import_export",
    "storages",
    "rest_framework_swagger",
    "drf_yasg",
)
LOCAL_APPS = (
    "accounts",
    "search",
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# END APP CONFIGURATION

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates/",
        ],
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



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]



# S3 Settings
LIARA_ENDPOINT="https://storage.c2.liara.space"
LIARA_BUCKET_NAME="saha"
LIARA_ACCESS_KEY="f0hl6d510ff2ekrp"
LIARA_SECRET_KEY="6d8cc809-cd15-43da-aa86-f54dddacb2d1"
# S3 Settings Based on AWS (optional)
AWS_ACCESS_KEY_ID = LIARA_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = LIARA_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = LIARA_BUCKET_NAME
AWS_S3_ENDPOINT_URL = LIARA_ENDPOINT
AWS_S3_REGION_NAME = 'us-east-1'


# Django-storages configuration
STORAGES = {
  "default": {
      "BACKEND": "storages.backends.s3.S3Storage",
  },
  "staticfiles": {
      "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
  },
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'





# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True



# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.getenv("STATIC_ROOT", default="/static/")
STATIC_URL = os.getenv("STATIC_URL", default="/static/")
MEDIA_ROOT = "https://saha.storage.c2.liara.space/media/"
MEDIA_URL = "https://saha.storage.c2.liara.space/media/"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# JWT SETIINGS
ACCESS_TTL = int(os.getenv("ACCESS_TTL", default="4"))  # days
REFRESH_TTL = int(os.getenv("REFRESH_TTL", default="10"))  # days
# END JWT SETTINGS



# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.backends.JWTAuthentication",
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_THROTTLE_RATES": {"otp": os.getenv("OTP_THROTTLE_RATE", default="10/min"), },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}




# END REST FRAMEWORK CONFIGURATION

MAX_UPLOAD_SIZE = 5242880

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Font', 'FontSize'],
            ['Bold', 'Italic'],
            ['TextColor', 'BGColor'],
            ['JustifyLeft', 'JustifyRight'],
            ['NumberedList', 'BulletedList'],
            ['Image', 'Flash', 'Table'],
            ['Source']
        ],
        'height': 100,
        'width': 650,
        'extraPlugins': 'justify',
    }
}

# CORSHEADERS CONFIGURATION
ALLOWED_HOSTS = ['127.0.0.1','0.0.0.0','liara.run','sahabackend.liara.run']
CORS_ALLOWED_ORIGINS = ["https://liara.run","http://127.0.0.1","https://sahabackend.liara.run"]
CSRF_TRUSTED_ORIGINS = ["https://liara.run","http://127.0.0.1","https://sahabackend.liara.run"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SECURE=True
CORS_ORIGIN_WHITELIST = ["https://liara.run","http://127.0.0.1","https://sahabackend.liara.run"]
# END CORSHEADERS CONFIGURATION
