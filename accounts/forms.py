from django.conf import settings
from django.contrib.auth import load_backend
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError
from django.forms.models import ModelForm

from accounts import utils


class UsernameCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 or password2:
            raise ValidationError("Do Not enter a password")
        return password2

    def save(self, commit=True):
        # Call super on parent class to overwrite the function
        user = super(UserCreationForm, self).save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class UsernameEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class UsernameLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UsernameLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    def clean(self):
        username = self.cleaned_data.get('username')
        if self.user_cache:
            self.user_cache = utils.authenticate_without_password(
                self.user_cache)
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
