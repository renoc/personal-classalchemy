from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from model_mommy import mommy
import mox


def create_view(viewclass):
    view = viewclass()
    view.request = RequestFactory()
    view.request.user = User.objects.create(username='testuser')
    return view
