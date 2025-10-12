import os

from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z-9wd4vh085_im9505wo_o7owy!kq)*kiavcls*60m9-k-r!x!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://localhost"]


# Application definition

INSTALLED_APPS = [
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # TOTP
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    # /TOTP
    "import_export",
    "leaderboard",
    "peer_review",
    "dashboard",
    "user_auth",
    "quests",
    "index",
    "user",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]


ROOT_URLCONF = "battlecode.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent.joinpath("templates")],
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

WSGI_APPLICATION = "battlecode.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),  # 12345,
        "HOST": os.environ.get("DB_HOST", default="localhost"),  # "localhost",
        "PORT": os.environ.get("DB_PORT", default=5432),  # 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

LOGIN_URL = "login"
OTP_LOGIN_URL = "/login/verify-otp/"


# Admin panel settings (SimpleUI)
SIMPLEUI_DEFAULT_THEME = "simpleui.css"
SIMPLEUI_DEFAULT_ICON = False

# Icons for Django Apps
SIMPLEUI_ICON = {
    "Otp_Static": "fa-solid fa-microchip",
    "Otp_Totp": "fa-solid fa-lock",
    "Static devices": "fa-solid fa-server",
    "TOTP devices": "fa-solid fa-lock",
    "Взятые задания": "fa-solid fa-tasks",
    "Quests": "fa-solid fa-map",
    "Квесты": "fa-solid fa-map",
    "Квесты - задачи": "fa-solid fa-list-check",
    "Навыки": "fa-solid fa-star",
    "Чек-листы ревью квеста": "fa-solid fa-clipboard-check",
    "Языки": "fa-solid fa-code",
}

SIMPLEUI_LOGIN_PARTICLES = True

# Custom home page (can be a link)
# SIMPLEUI_LOGO = "/static/favicon/logo.png"

# SimpleUI Info
SIMPLEUI_HOME_INFO = False

SIMPLEUI_HOME_QUICK = True

# SimpleUI Analysis (must be False)
SIMPLEUI_ANALYSIS = False

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR.parent.joinpath("collected_static")
STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.parent.joinpath("media")


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
