from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from model_mommy import mommy
import mox


def create_view(viewclass):
    user = User.objects.create(username='testuser')
    request = RequestFactory()
    request.user = user
    view = viewclass()
    view.request = request
    return view
