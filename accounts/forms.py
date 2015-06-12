from django.forms import ValidationError
from django.contrib.auth import _get_backends, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UsernameLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UsernameLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    def clean(self):
        username = self.cleaned_data.get('username')
        if self.user_cache:
            self.hack_backend()
            self.confirm_login_allowed(self.user_cache)
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
                self.user_cache = user
        return data

    def hack_backend(self):
        # This is a terrible hack, do not use if data is important
        assert(self.user_cache.is_staff is False)
        assert(self.user_cache.is_superuser is False)
        backend, backend_path = _get_backends(return_tuples=True)[0]
        self.user_cache.backend = backend_path
