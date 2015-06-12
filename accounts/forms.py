from django.conf import settings
from django.contrib.auth import load_backend
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError


class UsernameLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UsernameLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    def authenticate(self):
        for backend in settings.AUTHENTICATION_BACKENDS:
            user = self.user_cache
            if user == load_backend(backend).get_user(user.pk):
                self.user_cache.backend = backend
                return self.user_cache
        return None

    def clean(self):
        username = self.cleaned_data.get('username')
        if self.user_cache:
            self.authenticate()
            if hasattr(self.user_cache, 'backend'):
                self.confirm_login_allowed(self.user_cache)
            else:
                raise ImproperlyConfigured(
                    "Unexpected Authentication Error. Contact Admin.")
        return self.cleaned_data

    def clean_password(self):
        data = self.cleaned_data['password']
        if data:
            raise ValidationError("Do Not enter a password")
        try:
            username = self.cleaned_data['username']
            user = User.objects.get(username=username)
        except:
            raise ValidationError("User Does Not Exist")
        else:
            if user.has_usable_password():
                raise ValidationError("User Password is set")
            else:
                assert(user.is_staff is False)
                assert(user.is_superuser is False)
                self.user_cache = user
        return data
