from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **kwargs):
        return login_required(super(LoginRequiredMixin, cls).as_view(**kwargs))
