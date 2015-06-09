from django.http import HttpResponseRedirect

from config.settings import DEBUG


def ssl_required(view_func):
    def _checkssl(request, *args, **kwargs):
        if not DEBUG and not request.is_secure():
            request_url = request.build_absolute_uri(request.get_full_path())
            secure_url = request_url.replace('http://', 'https://')
            return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _checkssl
