from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from model_mommy import mommy
import mox

from dwclasses.models import CompendiumClass


def create_view(viewclass):
    user = User.objects.create(username='testuser')
    request = RequestFactory()
    request.user = user
    view = viewclass()
    view.request = request
    return view


class Model_Tests(TestCase):

    def test_get_or_404(self):
        # Use real implimentation for more robust test
        mod = CompendiumClass.objects.create(form_name='testcc')
        self.assertEqual(CompendiumClass.objects.get_or_404(id=mod.id), mod)
        self.assertRaises(Http404, CompendiumClass.objects.get_or_404, id=99)

    def test_get_user_classes(self):
        user = User(username='testuser')
        user.save()
        mod = CompendiumClass(form_name='testuni', user=user)
        mod.save()
        self.assertEqual(
            mod, CompendiumClass.objects.get_user_objects(user=user).get())
