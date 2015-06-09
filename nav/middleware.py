__author__ = '@danigosa'

from django.http import HttpResponsePermanentRedirect
from django.conf import settings

class SSLMiddleware(object):
    def __init__(self):
        self.paths = getattr(settings, 'SECURE_REQUIRED_PATHS')
        self.enabled = self.paths and getattr(settings, 'HTTPS_SUPPORT')
        self.DEBUG = getattr(settings, 'DEBUG')

    def process_request(self, request):
        if self.enabled and not self.DEBUG and not request.is_secure():
            for path in self.paths:
                if path in request.get_full_path():
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'https://')
                    return HttpResponsePermanentRedirect(secure_url)
        return None
