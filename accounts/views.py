from django.contrib import auth
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView, UpdateView

from accounts import utils
from accounts.forms import (
    UsernameCreationForm, UsernameEditForm, UsernameLoginForm)
from nav.models import LoginRequiredMixin


class CreateUserView(FormView):
    form_class = UsernameCreationForm
    success_url = '/dwclass/'
    template_name = 'user_create.html'

    def form_valid(self, form):
        user = form.save()
        user = utils.authenticate_without_password(user)
        auth.login(self.request, user)
        return super(CreateUserView, self).form_valid(form)


class EditUserView(LoginRequiredMixin, UpdateView):
    form_class = UsernameEditForm
    success_url = '/account/'
    template_name = "user_edit.html"

    def get_object(self):
        return self.request.user


class LoginView(FormView):
    form_class = UsernameLoginForm
    template_name = 'login.html'

    def get_success_url(self):
        self.success_url = self.request.GET.get('next', '/dwclass/')
        return super(LoginView, self).get_success_url()

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    permanent = False
    url = '/'

    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)
