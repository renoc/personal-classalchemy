from django.conf.urls import include, url
from django.contrib import admin
import views


admin.autodiscover()


urlpatterns = [
    url(r'^$', views.Home.as_view())
]
