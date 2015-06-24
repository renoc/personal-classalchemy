from django.conf.urls import include, url
from django.contrib import admin

from accounts import urls as accounts_urls
from dwclasses import urls as dwclasses_urls
from nav.decorators import ssl_required
from nav import urls as nav_urls


admin.autodiscover()


urlpatterns = nav_urls.urlpatterns + [
    url(r'^admin/', include(admin.site.urls)),
] + accounts_urls.urlpatterns + dwclasses_urls.urlpatterns
