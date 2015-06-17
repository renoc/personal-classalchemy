from django.http import Http404
from django.test import TestCase
from model_mommy import mommy
import mox

from dwclasses.models import CompendiumClass


class Model_Tests(TestCase):

    def test_get_or_404(self):
        # Use real implimentation for more robust test
        mod = CompendiumClass.objects.create(form_name='testcc')
        self.assertEqual(CompendiumClass.objects.get_or_404(id=mod.id), mod)
        self.assertRaises(Http404, CompendiumClass.objects.get_or_404, id=99)
