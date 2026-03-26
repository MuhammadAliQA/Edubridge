from pathlib import Path
import os
import warnings
from django.core.exceptions import ImproperlyConfigured

SKIP_DOTENV = os.environ.get('SKIP_DOTENV', 'False') == 'True'
if not SKIP_DOTENV:
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parent.parent / '.env')
    except ImportError:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-edubridge-change-in-production-2024')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]

ALLOWED_HOSTS = _split_csv(os.environ.get("ALLOWED_HOSTS", "*"))

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'courses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edubridge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

CSRF_FAILURE_VIEW = "edubridge.views.csrf_failure"

WSGI_APPLICATION = 'edubridge.wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL')
REQUIRE_DATABASE_URL = os.environ.get('REQUIRE_DATABASE_URL', 'False') == 'True'
if DATABASE_URL and DEBUG:
    allow_remote_db_in_debug = os.environ.get("ALLOW_REMOTE_DB_IN_DEBUG", "False") == "True"
    if (not allow_remote_db_in_debug) and ("render.com" in DATABASE_URL):
        warnings.warn(
            "DATABASE_URL points to Render; using local SQLite in DEBUG. "
            "Set ALLOW_REMOTE_DB_IN_DEBUG=True to override.",
            RuntimeWarning,
        )
        DATABASE_URL = None
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    if REQUIRE_DATABASE_URL:
        raise ImproperlyConfigured("DATABASE_URL is required when DEBUG=False (configure PostgreSQL).")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'auth.User'

LOGIN_URL = '/kirish/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

IS_PROD = (not DEBUG) and (
    os.environ.get("REQUIRE_SECRET_KEY", "False") == "True"
    or os.environ.get("REQUIRE_DATABASE_URL", "False") == "True"
)

if not DEBUG:
    if IS_PROD and (
        SECRET_KEY.startswith("django-insecure-")
        or SECRET_KEY == "django-insecure-edubridge-change-in-production-2024"
    ):
        raise ImproperlyConfigured("SECRET_KEY must be set in production.")

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True") == "True"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "True") == "True"
    CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True") == "True"

    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False") == "True"
    SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False") == "True"

    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    REFERRER_POLICY = os.environ.get("REFERRER_POLICY", "same-origin")

    csrf_origins = _split_csv(os.environ.get("CSRF_TRUSTED_ORIGINS", ""))
    render_hostname = (os.environ.get("RENDER_EXTERNAL_HOSTNAME") or "").strip()
    if render_hostname:
        csrf_origins.append(f"https://{render_hostname}")
    CSRF_TRUSTED_ORIGINS = sorted(set(csrf_origins))

    if IS_PROD and ("*" in ALLOWED_HOSTS or not ALLOWED_HOSTS):
        render_hostname = (os.environ.get("RENDER_EXTERNAL_HOSTNAME") or "").strip()
        if render_hostname:
            ALLOWED_HOSTS = [render_hostname]
        else:
            raise ImproperlyConfigured("Set ALLOWED_HOSTS in production (comma-separated).")

# ============ JAZZMIN ADMIN ============
JAZZMIN_SETTINGS = {
    "site_title": "EduBridge Admin",
    "site_header": "EduBridge",
    "site_brand": "EduBridge",
    "site_icon": None,
    "welcome_sign": "EduBridge Admin Paneliga Xush Kelibsiz",
    "copyright": "EduBridge © 2025",

    "topmenu_links": [
        {"name": "Sayt", "url": "/", "new_window": True},
        {"name": "Mentorlar", "url": "/mentorlar/", "new_window": True},
        {"name": "Grants", "url": "/grants/", "new_window": True},
    ],

    "usermenu_links": [
        {"name": "Saytga qaytish", "url": "/", "new_window": True},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.MentorProfile": "fas fa-chalkboard-teacher",
        "accounts.StudentProfile": "fas fa-user-graduate",
        "accounts.Enrollment": "fas fa-book-open",
        "courses.Kurs": "fas fa-graduation-cap",
        "courses.FreeDars": "fas fa-video",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-orange",
    "accent": "accent-orange",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-orange",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "default_theme_mode": "dark",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
