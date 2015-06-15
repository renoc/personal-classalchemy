from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.list import ListView
from model_mommy import mommy
import mox

from dwclasses.models import (
    ClassChoice, CombinedClass, CompendiumClassManager, CompendiumClass,
    CompletedCharacter)
from dwclasses.views import ListCompendiumClassesView


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


class ClassChoice_ModelTests(TestCase):

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


class CompendiumClass_ModelTests(TestCase):

    def test_name_property(self):
        testname = 'testname'
        mod = CompendiumClass(form_name=testname)
        self.assertEqual(mod.name, testname)

    def test_get_list(self):
        user = User(username='testuser')
        user.save()
        mod = CompendiumClass(form_name='testuni', user=user)
        mod.save()
        self.assertEqual(
            mod, CompendiumClass.objects.get_list(user=user).get())


class View_Tests(TestCase):
    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_list_compendium_classes_view(self):
        user = User(username='testuser')
        request = RequestFactory()
        request.user = user
        view = ListCompendiumClassesView()
        view.request = request

        self.moxx.StubOutWithMock(CompendiumClassManager, 'get_list')
        CompendiumClassManager.get_list(user=user).AndReturn(None)
        self.moxx.StubOutWithMock(ListView, 'get_queryset')
        ListView.get_queryset().AndReturn(None)

        self.moxx.ReplayAll()
        view.get_queryset()
        self.moxx.VerifyAll()

        # all mocked functions called
