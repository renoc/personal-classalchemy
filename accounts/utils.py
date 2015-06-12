from django.conf import settings
from django.contrib.auth import load_backend


def authenticate_without_password(user):
    for backend in settings.AUTHENTICATION_BACKENDS:
        if user == load_backend(backend).get_user(user.pk):
            user.backend = backend
            return user
    return None
