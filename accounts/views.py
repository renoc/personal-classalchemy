from django.contrib.auth import login
from django.views.generic.edit import FormView

from accounts.forms import UsernameLoginForm


class LoginView(FormView):
    form_class = UsernameLoginForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)
