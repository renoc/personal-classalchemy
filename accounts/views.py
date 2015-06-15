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
    template_name = 'login.html'

    def get_success_url(self):
        self.success_url = self.request.GET.get('next', '/compendiumclasses/')
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
