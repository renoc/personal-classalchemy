from django.conf.urls import include, url

from nav.decorators import ssl_required
import accounts.views as views


urlpatterns = [
    url(r'^create_user', ssl_required(views.CreateUserView.as_view())),
    url(r'^login', ssl_required(views.LoginView.as_view())),
    url(r'^logout', ssl_required(views.LogoutView.as_view())),
]
