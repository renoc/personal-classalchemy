from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from dwclasses.models import (
    ClassChoice, CombinedClass, CompendiumClass, CompletedCharacter)


class Unicode_Tests(TestCase):

    def test_ClassChoice(self):
        mod = ClassChoice(field_name='testuni')
        self.assertEqual('testuni', '%s' % mod)
        mod.user = mommy.make(User, username='testuser')
        self.assertEqual('testuser - testuni', '%s' % mod)

    def test_CombinedClass(self):
        mod = CombinedClass(form_name='testuni')
        self.assertEqual('testuni', '%s' % mod)
        mod.user = mommy.make(User, username='testuser')
        self.assertEqual('testuser - testuni', '%s' % mod)

    def test_CompendiumClass(self):
        mod = CompendiumClass(form_name='testuni')
        self.assertEqual('testuni', '%s' % mod)
        mod.user = mommy.make(User, username='testuser')
        self.assertEqual('testuser - testuni', '%s' % mod)

    def test_CompletedCharacter(self):
        mod = CompletedCharacter(form_name='testuni')
        self.assertEqual('testuni', '%s' % mod)
        mod.user = mommy.make(User, username='testuser')
        self.assertEqual('testuser - testuni', '%s' % mod)

class ClassChoice_Tests(TestCase):

    def test_validate_pass(self):
        mod = mommy.make(ClassChoice, field_name='testuni')
        mod.save()
        mod.validate_unique()
        #No errors raised

    def test_validate_fail(self):
        mod = mommy.make(ClassChoice, field_name='testuni')
        mod.save()
        mod = mommy.make(ClassChoice, field_name='testuni')
        self.assertRaises(ValidationError, mod.validate_unique())
