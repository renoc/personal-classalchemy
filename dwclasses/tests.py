from combinedchoices.models import ChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.list import ListView
from model_mommy import mommy
import mox

from dwclasses.forms import CompendiumClassForm
from dwclasses.models import (
    ClassChoice, CombinedClass, CompendiumClassManager, CompendiumClass,
    CompletedCharacter)
from dwclasses.views import (
    CreateCompendiumClassView, EditCompendiumClassView,
    ListCompendiumClassesView)


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

    def test_get_user_classes(self):
        user = User(username='testuser')
        user.save()
        mod = CompendiumClass(form_name='testuni', user=user)
        mod.save()
        self.assertEqual(
            mod, CompendiumClass.objects.get_user_classes(user=user).get())

    def test_unlinked_choices(self):
        user = mommy.make(User, username='testuser')
        tested = mommy.make(CompendiumClass, form_name='tested', user=user)
        untested = mommy.make(CompendiumClass, form_name='untested', user=user)
        modin = mommy.make(ClassChoice, field_name='in', user=user)
        modout = mommy.make(ClassChoice, field_name='out', user=user)
        modother = mommy.make(ClassChoice, field_name='other')
        mommy.make(ChoiceField, base_ccobj=tested, base_choice=modin)
        mommy.make(ChoiceField, base_ccobj=untested, base_choice=modout)
        self.assertEqual(tested.available_choices().get(), modout)


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

        self.moxx.StubOutWithMock(CompendiumClassManager, 'get_user_classes')
        CompendiumClassManager.get_user_classes(user=user).AndReturn(None)
        self.moxx.StubOutWithMock(ListView, 'get_queryset')
        ListView.get_queryset().AndReturn(None)

        self.moxx.ReplayAll()
        view.get_queryset()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_create_compendium_get_success_url(self):
        view = CreateCompendiumClassView()
        view.object = CompendiumClass(form_name='testcc', id=99)
        self.assertTrue(view.get_success_url(), "/compendiumclasses/99")

    def test_create_compendium_class_form_valid(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = CreateCompendiumClassView()
        view.request = request
        comp = CompendiumClassForm()
        comp.cleaned_data = {'form_name': 'testcc'}

        self.moxx.StubOutWithMock(CreateCompendiumClassView, 'get_success_url')
        CreateCompendiumClassView.get_success_url().AndReturn(None)

        self.assertFalse(CompendiumClass.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=comp)
        self.moxx.VerifyAll()

        self.assertTrue(CompendiumClass.objects.all().exists())

    def test_edit_compendium_class_get_object(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = EditCompendiumClassView()
        view.request = request
        view.kwargs = {'cc_id': 0}

        self.moxx.StubOutWithMock(CompendiumClassManager, 'get_or_404')
        CompendiumClassManager.get_or_404(id=0, user=user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_object()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_edit_compendium_class_success_url(self):
        view = EditCompendiumClassView()
        view.object = CompendiumClass(form_name='testcc', id=99)
        self.assertTrue(view.get_success_url(), "/compendiumclasses/99")
