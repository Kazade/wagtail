"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from djangae.settings_base import *  # Set up some AppEngine specific stuff
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

from .boot import get_app_config
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_app_config().secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = (
    'djangae',  # Djangae needs to come before django apps in django 1.7 and above
    
    '{{ project_name }}',
    'home',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'taggit',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'djangae.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',
    'cspreports',
    'djangae.contrib.gauth.datastore',
    'djangae.contrib.security',
    # 'djangae.contrib.uniquetool',
)

MIDDLEWARE_CLASSES = (
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'djangae.contrib.gauth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'csp.middleware.CSPMiddleware',
    'session_csrf.CsrfMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.core.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "session_csrf.context_processor"
            ],
            'debug': True,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

SILENCED_SYSTEM_CHECKS = [
    'security.W003',  # We're using session_csrf version of CsrfMiddleware, so we can skip that check
]
from .boot import register_custom_checks
register_custom_checks()

CSP_REPORT_URI = reverse_lazy('report_csp')
CSP_REPORTS_LOG = True
CSP_REPORTS_LOG_LEVEL = 'warning'
CSP_REPORTS_SAVE = True
CSP_REPORTS_EMAIL_ADMINS = False

ROOT_URLCONF = '{{ project_name }}.urls'

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# sensible default CSP settings, feel free to modify them
CSP_DEFAULT_SRC = ("'self'", "*.gstatic.com")
# Inline styles are unsafe, but Django error pages use them. We later remove
# `unsafe-inline` in settings_live.py
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "fonts.googleapis.com", "*.gstatic.com")
CSP_FONT_SRC = ("'self'", "themes.googleusercontent.com", "*.gstatic.com")
CSP_FRAME_SRC = ("'self'", "www.google.com", "www.youtube.com", "accounts.google.com", "apis.google.com", "plus.google.com")
CSP_SCRIPT_SRC = ("'self'", "*.googleanalytics.com", "*.google-analytics.com", "ajax.googleapis.com")
CSP_IMG_SRC = ("'self'", "data:", "s.ytimg.com", "*.googleusercontent.com", "*.gstatic.com", "www.google-analytics.com")
CSP_CONNECT_SRC = ("'self'", "plus.google.com", "www.google-analytics.com")
CSP_EXCLUDE_URL_PREFIXES = "/admin/"  # Wagtail admin exception

from djangae.contrib.gauth.settings import *

# Wagtail settings

WAGTAIL_SITE_NAME = "{{ project_name }}"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'


# Djangae doesn't use a Permission model to record individual permissions, instead it uses strings inside a ListField
# stored on the object, e.g. User or Group.
#
# Because of this, listing all available permissions or permissions for a particular model is not possible. To overcome
# this Djangae generates the usual model permissions at runtime ('add', 'change', 'delete') and augments this with any
# custom permissions listed here:
#
# Add custom auto-generated permissions here that are applied to all models. E.g. adding custom 'copy' permission would
# allow '[app_label].copy_[model]' permission in all models.
# AUTOGENERATED_PERMISSIONS = ('add', 'change', 'delete')
#
# One-off custom permissions:
MANUAL_PERMISSIONS = [
    ('wagtailadmin.access_admin', _('Can access Wagtail admin')),
    ('wagtailcore.publish_page', _("Publish any page")),
    ('wagtailcore.lock_page', _("Lock/unlock any page")),

]