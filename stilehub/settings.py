from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-!4!4ig26uhu1pihy46vzbi599-s$0he&$+7%6*9p1-o+^!bva_'
DEBUG = True
ALLOWED_HOSTS = []

# ==================== Приложения ====================
INSTALLED_APPS = [
    'jazzmin',
    'pages',
    'accounts',
    'shop',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# Настройки Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "StyleHub Admin",
    "site_header": "StyleHub 🕶️",
    "site_brand": "StyleHub",
    "welcome_sign": "Добро пожаловать в админку StyleHub",
    "copyright": "StyleHub © 2025",
    "search_model": "shop.Product",
    "topmenu_links": [
        {"name": "Главная сайт",  "url": "/", "new_window": True},
        {"model": "auth.user"},
        {"app": "shop"}
    ],
    "show_language_selector": True,
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "actions_sticky_top": True,
}
# ==================== Middleware ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'stilehub.urls'

# ==================== Templates ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # добавляем глобальную папку templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart_item_count',  # корзина
            ],
        },
    },
]

WSGI_APPLICATION = 'stilehub.wsgi.application'

# ==================== База данных ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================== Валидация пароля ====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ==================== Локализация ====================
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

import os
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
    ('uk', 'Український')

]


# ==================== Статика ====================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # для деплоя

# ==================== Медиа ====================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"  # куда будут загружаться аватары и файлы

# ==================== Дефолтный PK ====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== Логин редиректы ====================
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'index'
