from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
import session_csrf

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch import urls as wagtailsearch_urls


session_csrf.monkeypatch()

urlpatterns = (
    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^django-admin/', include(admin.site.urls)),
    
    url(r'^csp/', include('cspreports.urls')),
    
    # Djangae
    url(r'^_ah/', include('djangae.urls')),
    url(r'^auth/', include('djangae.contrib.gauth.urls')),
    
    # Wagtail
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/', include(wagtailsearch_urls)),
    url(r'', include(wagtail_urls)),
)
