"""
Django settings — HealthAnalytics IPS
Lee credenciales desde variables de entorno (.env)
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Seguridad ─────────────────────────────────────────────────
SECRET_KEY = os.getenv('SECRET_KEY', 'cambia-esta-clave-en-produccion')
DEBUG      = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if os.getenv('CSRF_TRUSTED_ORIGINS') else []

# ── Aplicaciones ──────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',       # Swagger / OpenAPI

    # Apps locales
    'authentication',
    'patients',
    'etl',
    'analytics',
    'ml',
    'dashboard',
]

# ── Middleware ────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# ── Base de datos ─────────────────────────────────────────────
import re

_DATABASE_URL = os.getenv('DATABASE_URL', '')
if _DATABASE_URL:
    m = re.match(r'postgres(?:ql)?://(.+?):(.+?)@(.+?):(\d+)/(.+?)(\?.*)?$', _DATABASE_URL)
    if m:
        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.postgresql',
                'NAME':     m.group(5),
                'USER':     m.group(1),
                'PASSWORD': m.group(2),
                'HOST':     m.group(3),
                'PORT':     m.group(4),
                'OPTIONS':  {'sslmode': 'require'},
            }
        }
    else:
        print(f'⚠️  DATABASE_URL found but could not parse: {_DATABASE_URL[:50]}...')
        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.postgresql',
                'NAME':     os.getenv('DB_NAME',     'neondb'),
                'USER':     os.getenv('DB_USER',     'neondb_owner'),
                'PASSWORD': os.getenv('DB_PASSWORD', ''),
                'HOST':     os.getenv('DB_HOST',     'localhost'),
                'PORT':     os.getenv('DB_PORT',     '5432'),
                'OPTIONS':  {'sslmode': 'require'},
            }
        }
else:
    print('⚠️  DATABASE_URL is not set, using defaults')
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     os.getenv('DB_NAME',     'neondb'),
            'USER':     os.getenv('DB_USER',     'neondb_owner'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST':     os.getenv('DB_HOST',     'localhost'),
            'PORT':     os.getenv('DB_PORT',     '5432'),
            'OPTIONS':  {'sslmode': 'require'},
        }
    }

# ── Validación de contraseñas ─────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internacionalización ──────────────────────────────────────
LANGUAGE_CODE = 'es-co'
TIME_ZONE     = 'America/Bogota'
USE_I18N      = True
USE_TZ        = True

# ── Archivos estáticos ────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'build' / 'static',
] if (BASE_DIR / 'frontend' / 'build' / 'static').exists() else []

# ── CORS ──────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if os.getenv('CORS_ALLOWED_ORIGINS') else []

# ── Django REST Framework ─────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ── JWT ───────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# ── Swagger / OpenAPI ─────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE':       'HealthAnalytics IPS — API',
    'DESCRIPTION': (
        'Plataforma Inteligente de Analítica Clínica para Detección de Riesgo Médico. '
        'Incluye ETL, analítica estadística, Machine Learning y gestión de pacientes. '
        'Todos los endpoints requieren autenticación JWT — usa /api/token/ para obtener el token '
        'y luego Authorize con el formato: Bearer <token>'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Sara Lucía Cervantes',
    },
    'LICENSE': {'name': 'Proyecto Educativo SENA 2026'},
    'TAGS': [
        {'name': 'Autenticación',  'description': 'Login y tokens JWT'},
        {'name': 'Pacientes',      'description': 'CRUD de pacientes clínicos'},
        {'name': 'Dashboard',      'description': 'KPIs y datos para gráficas'},
        {'name': 'ETL',            'description': 'Pipeline ETL e historial de ejecuciones'},
        {'name': 'Analytics',      'description': 'Estadísticas descriptivas y segmentación'},
        {'name': 'Machine Learning','description': 'Entrenamiento, métricas y predicción'},
        {'name': 'Reportes',       'description': 'Reportes generales del sistema'},
    ],
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}

# ── Clave primaria por defecto ────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'