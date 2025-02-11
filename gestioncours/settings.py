from pathlib import Path
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Fonction pour récupérer une variable d'environnement avec gestion d'erreur
def get_env_variable(var_name, default=None, required=False):
    value = os.getenv(var_name, default)
    if required and value is None:
        raise ImproperlyConfigured(f"La variable d'environnement {var_name} est manquante ! Vérifiez votre fichier .env.")
    return value

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Récupération des variables d'environnement avec gestion d'erreur
SECRET_KEY = get_env_variable('SECRET_KEY', required=True)
DEBUG = get_env_variable('DEBUG', 'False').lower() in ['true', '1']
ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'inscriptions',
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

ROOT_URLCONF = 'gestioncours.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [BASE_DIR / 'inscriptions/templates'],
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

WSGI_APPLICATION = 'gestioncours.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('DB_NAME', required=True),
        'USER': get_env_variable('DB_USER', required=True),
        'PASSWORD': get_env_variable('DB_PASSWORD', required=True),
        'HOST': get_env_variable('DB_HOST', 'localhost'),
        'PORT': get_env_variable('DB_PORT', '3306'),
    }
}





# Password validation
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

# Configuration des messages Django
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuration email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = get_env_variable('EMAIL_PORT', '587')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', required=True)
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD', required=True)
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL', 'elconquistadorbaoulyn@gmail.com')

# Static & Media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Ajoute cette ligne pour définir où les fichiers statiques seront collectés
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# URLs de redirection
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Redirection après connexion
LOGIN_REDIRECT_URL = '/profile/'

# Redirection après déconnexion (optionnel)
LOGOUT_REDIRECT_URL = '/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
