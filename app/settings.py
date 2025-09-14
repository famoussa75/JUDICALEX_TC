from pathlib import Path
import os
from django.shortcuts import redirect
from django.urls import resolve

# ==========================================
# BASE DIRECTORY
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# MIDDLEWARE LOGIN REQUIRED
# ==========================================
class LoginRequiredMiddleware:
    """
    Middleware pour rediriger les utilisateurs non authentifiés vers la page de connexion.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Liste des URL ou préfixes à exclure
        excluded_paths = ['/login/', '/admin/', '/static/', '/media/']

        # Vérifie si l'utilisateur est authentifié ou si le chemin est exclu
        if not request.user.is_authenticated and not any(request.path.startswith(path) for path in excluded_paths):
            # Redirige vers la page de connexion
            return redirect('login')

        return self.get_response(request)


# ==========================================
# SECURITY
# ==========================================
SECRET_KEY = 'django-insecure-3xav8ay3z^!$&ui0!+hnxofu57gwr6l1mdo4-%a0&zch__q8%w'
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.68.101', '192.168.90.14']


# ==========================================
# APPLICATIONS
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications du projet
    'account.apps.AccountConfig',
    '_base',
    'rccm',
    'role',
    'magistrats',
]

AUTH_USER_MODEL = 'account.Account'


# ==========================================
# MIDDLEWARE
# ==========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware perso
    'account.middleware.LoginRequiredMiddleware',
]


# ==========================================
# URLS & WSGI
# ==========================================
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'


# ==========================================
# TEMPLATES
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


# ==========================================
# DATABASE
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 't_commerce_db',
        'USER': 'famoussa',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}


# ==========================================
# PASSWORDS
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================
# INTERNATIONALIZATION
# ==========================================
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==========================================
# STATIC & MEDIA FILES
# ==========================================
STATIC_URL = '/static/'

# En local, on peut avoir des fichiers dans BASE_DIR/static
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# En production, collectstatic les envoie ici
STATIC_ROOT = BASE_DIR / "staticfiles"

# Gestion des fichiers médias
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Setting perso : choix auto du dossier statique de base (utile pour ReportLab)
if STATICFILES_DIRS:
    STATICFILES_BASE_DIR = STATICFILES_DIRS[0]
else:
    STATICFILES_BASE_DIR = STATIC_ROOT


# ==========================================
# AUTRES
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
