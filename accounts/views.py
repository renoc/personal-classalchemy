from django.contrib import auth
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from accounts import utils
from accounts.forms import UsernameCreationForm, UsernameLoginForm


class CreateUserView(FormView):
    form_class = UsernameCreationForm
    success_url = '/'
    template_name = 'create_user.html'

    def form_valid(self, form):
        user = form.save()
        user = utils.authenticate_without_password(user)
        auth.login(self.request, user)
        return super(CreateUserView, self).form_valid(form)


class LoginView(FormView):
    form_class = UsernameLoginForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    permanent = False
    url = '/'

    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)
