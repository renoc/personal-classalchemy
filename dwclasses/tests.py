from combinedchoices.models import ChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from django.views.generic.list import ListView
from model_mommy import mommy
import mox

from dwclasses.forms import CompendiumClassForm, SectionForm
from dwclasses.models import (
    CombinedClass, CompendiumClassManager, CompendiumClass,
    CompletedCharacter, SectionManager, Section)
from dwclasses.views import (
    ListCompendiumClassesView, CreateCompendiumClassView,
    EditCompendiumClassView,
    CreateSectionView, EditSectionView, RemoveSectionView, LinkSectionView)


class Unicode_Tests(TestCase):

    def test_Section(self):
        mod = Section(field_name='testuni')
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


class Section_ModelTests(TestCase):

    def test_validate_pass(self):
        mod = mommy.make(Section, field_name='testuni')
        mod.save()
        mod.validate_unique()
        #No errors raised

    def test_validate_fail(self):
        mod = mommy.make(Section, field_name='testuni')
        mod.save()
        mod = mommy.make(Section, field_name='testuni')
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
        modin = mommy.make(Section, field_name='in', user=user)
        modout = mommy.make(Section, field_name='out', user=user)
        modother = mommy.make(Section, field_name='other')
        mommy.make(ChoiceField, base_ccobj=tested, base_choice=modin)
        mommy.make(ChoiceField, base_ccobj=untested, base_choice=modout)
        self.assertEqual(tested.available_sections().get(), modout)


class Compendium_View_Tests(TestCase):
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


class Section_View_Tests(TestCase):

    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_mixin_get_context(self):
        view = EditSectionView()

        self.moxx.StubOutWithMock(FormMixin, 'get_context_data')
        FormMixin.get_context_data().AndReturn({})
        self.moxx.StubOutWithMock(EditSectionView, 'get_compendium_class')
        EditSectionView.get_compendium_class().AndReturn('foo')

        self.moxx.ReplayAll()
        context = view.get_context_data()
        self.moxx.VerifyAll()

        self.assertEqual(context['compendium_class'], 'foo')

    def test_mixin_get_compendium_class(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = EditSectionView()
        view.request = request
        view.kwargs = {'cc_id': 0}

        self.moxx.StubOutWithMock(CompendiumClassManager, 'get_or_404')
        CompendiumClassManager.get_or_404(id=0, user=user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_compendium_class()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_mixin_get_section(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = EditSectionView()
        view.request = request
        view.kwargs = {'sec_id': 0}

        self.moxx.StubOutWithMock(SectionManager, 'get_or_404')
        SectionManager.get_or_404(id=0, user=user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_section()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_create_section_success_url(self):
        view = CreateSectionView()
        view.object = mommy.make(Section, id=99)
        view.kwargs = {'cc_id': 0}

        self.moxx.StubOutWithMock(CreateView, 'get_success_url')
        CreateView.get_success_url().AndReturn(None)

        self.moxx.ReplayAll()
        view.get_success_url()
        self.moxx.VerifyAll()

        self.assertTrue(
            view.success_url, "/compendiumclasses/0/edit_section/99")

    def test_create_section_valid(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = CreateSectionView()
        view.request = request
        form = SectionForm()
        comp = mommy.make(CompendiumClass)
        sec = Section(field_type=0)

        self.moxx.StubOutWithMock(CreateSectionView, 'get_compendium_class')
        CreateSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(SectionForm, 'save')
        SectionForm.save(commit=False).AndReturn(sec)
        self.moxx.StubOutWithMock(CreateSectionView, 'get_success_url')
        CreateSectionView.get_success_url().AndReturn(None)

        self.assertFalse(ChoiceField.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=form)
        self.moxx.VerifyAll()

        self.assertTrue(ChoiceField.objects.all().exists())

    def test_edit_section_get_object(self):
        view = EditSectionView()

        self.moxx.StubOutWithMock(EditSectionView, 'get_section')
        EditSectionView.get_section().AndReturn(None)

        self.moxx.ReplayAll()
        view.get_object()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_edit_section_success_url(self):
        request = RequestFactory()
        view = EditSectionView()
        view.request = request
        view.kwargs = {'cc_id': 0}
        sec = mommy.make(Section)
        view.object = sec

        self.moxx.StubOutWithMock(UpdateView, 'get_success_url')
        UpdateView.get_success_url().AndReturn(None)

        self.moxx.ReplayAll()
        view.get_success_url()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_remove_section(self):
        request = RequestFactory()
        view = RemoveSectionView()
        view.request = request
        comp = mommy.make(CompendiumClass)
        sec = mommy.make(Section)
        ChoiceField.objects.create(base_ccobj=comp, base_choice=sec)

        self.assertTrue(ChoiceField.objects.all().exists())

        self.moxx.StubOutWithMock(RemoveSectionView, 'get_compendium_class')
        RemoveSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(RemoveSectionView, 'get_section')
        RemoveSectionView.get_section().AndReturn(sec)

        self.moxx.ReplayAll()
        view.get_redirect_url()
        self.moxx.VerifyAll()

        self.assertFalse(ChoiceField.objects.all().exists())

    def test_linksection_getsection(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.POST = {'sec_id': 0}
        request.user = user
        view = LinkSectionView()
        view.request = request

        self.moxx.StubOutWithMock(SectionManager, 'get_or_404')
        SectionManager.get_or_404(id=0, user=user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_section()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_link_existing_section(self):
        request = RequestFactory()
        view = LinkSectionView()
        view.request = request
        comp = mommy.make(CompendiumClass)
        sec = mommy.make(Section)

        self.assertFalse(ChoiceField.objects.all().exists())

        self.moxx.StubOutWithMock(LinkSectionView, 'get_compendium_class')
        LinkSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(LinkSectionView, 'get_section')
        LinkSectionView.get_section().AndReturn(sec)

        self.moxx.ReplayAll()
        view.get_redirect_url()
        self.moxx.VerifyAll()

        self.assertTrue(ChoiceField.objects.all().exists())
