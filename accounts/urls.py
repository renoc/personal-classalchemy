from django.conf.urls import include, url

from nav.decorators import ssl_required
import accounts.views as views


urlpatterns = [
    url(r'^login', ssl_required(views.LoginView.as_view()))
]
