"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import environ
import os
import dj_database_url
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Ensure OpenAI Key is ensured
OPENAI_API_KEY = env("OPENAI_API_KEY", default=None)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)


ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    # Add Whitenoise here
    'whitenoise.runserver_nostatic', 
    
    # Styling
    'tailwind',
    'theme', # Tailwind theme app

    
    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Google OAuth
    
    # Custom apps
    'accounts',
    'recipes',
    'profiles',
    'explore', 
    
    # Google Storage for images
    'storages',
]


AUTH_USER_MODEL = 'accounts.CustomUser'


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth authentication
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
     # Add Whitenoise middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
     # Required for Django Allauth
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ACCOUNT_LOGOUT_TEMPLATE = "account/logout.html"


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=env("DATABASE_URL")
    )
}




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# Enable static files compression & caching for production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Social Authentication Settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account'  # Forces a fresh login in an external browser
            },
        'OAUTH_PKCE_ENABLED': True, 
        'APP': {
            'client_id': env("GOOGLE_CLIENT_ID"),
            'secret': env("GOOGLE_CLIENT_SECRET"),
        },
    }
}



# Use email as the primary identifier
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False  
ACCOUNT_UNIQUE_EMAIL = True  # Ensure unique emails
ACCOUNT_EMAIL_VERIFICATION = "optional"  # Or set to "mandatory" if needed


# Site ID for Django Allauth (Required)
SITE_ID = 1


# Redirects after login/logout
LOGIN_REDIRECT_URL = '/'  # Redirect after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # Redirect after logout


# Allow users to sign in with Google even if their email exists
ACCOUNT_ADAPTER = "accounts.adapters.NoPasswordAccountAdapter"
SOCIALACCOUNT_ADAPTER = "accounts.adapters.MySocialAccountAdapter"


# Enable automatic linking of Google accounts with existing accounts
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"  # Or "mandatory" if you want email confirmation
SOCIALACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True  # Ensures unique emails
ACCOUNT_LOGIN_METHODS = {'email'}  # Authenticate via email


# Styling app for Tailwind
TAILWIND_APP_NAME = "theme"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


TIME_ZONE = 'America/Chicago'  

# === Google Cloud Storage for Media Files ===
if not DEBUG:
    GS_BUCKET_NAME = env('GS_BUCKET_NAME')

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_BUCKET_NAME,
                "default_acl": "publicRead",
                "cache_control": "public, max-age=86400",
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"



