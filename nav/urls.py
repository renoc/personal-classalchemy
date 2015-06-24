from django.conf.urls import include, url

import accounts.urls as accounts_urls
import nav.views as views


urlpatterns = [
    url(r'^($|index)', views.Home.as_view()),
    url(r'^about', views.About.as_view()),
    url(r'^paq', views.PAQ.as_view()),
]
