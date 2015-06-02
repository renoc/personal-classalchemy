from django.conf.urls import include, url
import nav.views as views


urlpatterns = [
    url(r'^($|index)', views.Home.as_view())
]
