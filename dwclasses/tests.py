from combinedchoices.models import ChoiceSection
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.edit import (
    CreateView, FormView, FormMixin, UpdateView)
from django.views.generic.list import ListView
from extra_views.advanced import UpdateWithInlinesView
from model_mommy import mommy
import mox

from config.models import UserModelManager
from dwclasses.forms import (
    CompendiumClassForm, SectionForm, ChoiceSectionForm, ChoiceForm,
    CombineForm)
from dwclasses.models import (
    CombinedClass, CompendiumClass, CompletedCharacter, Section)
from dwclasses.views import (
    ListCompendiumClassesView, CreateCompendiumClassView,
    EditCompendiumClassView, CreateSectionView, EditSectionInlineView,
    RemoveSectionView, LinkSectionView, ListCombinedClassesView,
    CreateCombinedClassView, EditCombinedClassView, NewCharacterView)


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

    def test_name_property_combined(self):
        testname = 'testname'
        mod = CombinedClass(form_name=testname)
        self.assertEqual(mod.name, testname)

    def test_unlinked_choices(self):
        user = mommy.make(User, username='testuser')
        tested = mommy.make(CompendiumClass, form_name='tested', user=user)
        untested = mommy.make(CompendiumClass, form_name='untested', user=user)
        modin = mommy.make(Section, field_name='in', user=user)
        modout = mommy.make(Section, field_name='out', user=user)
        modother = mommy.make(Section, field_name='other')
        mommy.make(ChoiceSection, base_ccobj=tested, base_choice=modin)
        mommy.make(ChoiceSection, base_ccobj=untested, base_choice=modout)
        self.assertEqual(tested.available_sections().get(), modout)


class CompletedCharacter_ModelTests(TestCase):

    def test_return_data(self):
        mod = mommy.make(CompletedCharacter, form_name='testuni')
        mod = CompletedCharacter.objects.get(id=mod.id)
        self.assertFalse(type(mod.form_data) is dict)  # String
        self.assertTrue(type(mod.data()) is dict)


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

        self.moxx.StubOutWithMock(UserModelManager, 'get_user_objects')
        UserModelManager.get_user_objects(user=user).AndReturn(None)
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

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(id=0, user=user).AndReturn(None)

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
        view = EditSectionInlineView()

        self.moxx.StubOutWithMock(FormMixin, 'get_context_data')
        FormMixin.get_context_data().AndReturn({})
        self.moxx.StubOutWithMock(EditSectionInlineView, 'get_compendium_class')
        EditSectionInlineView.get_compendium_class().AndReturn('foo')

        self.moxx.ReplayAll()
        context = view.get_context_data()
        self.moxx.VerifyAll()

        self.assertEqual(context['compendium_class'], 'foo')

    def test_mixin_get_compendium_class(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = EditSectionInlineView()
        view.request = request
        view.kwargs = {'cc_id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(id=0, user=user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_compendium_class()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_mixin_get_section(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = EditSectionInlineView()
        view.request = request
        view.kwargs = {'sec_id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(id=0, user=user).AndReturn(None)

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

        self.assertFalse(ChoiceSection.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=form)
        self.moxx.VerifyAll()

        self.assertTrue(ChoiceSection.objects.all().exists())

    def test_edit_section_get_form_subforms(self):
        view = EditSectionInlineView()

        self.moxx.StubOutWithMock(EditSectionInlineView, 'get_form_kwargs')
        self.moxx.StubOutWithMock(UpdateWithInlinesView, 'get_form')
        UpdateWithInlinesView.get_form(ChoiceForm).AndReturn(None)

        self.moxx.ReplayAll()
        form = view.get_form(ChoiceForm)
        self.moxx.VerifyAll()

        # proper mocked functions called

    def test_edit_section_get_form_mainform(self):
        view = EditSectionInlineView()
        comp = mommy.make(CompendiumClass)
        sec = mommy.make(Section)
        choicef = mommy.make(ChoiceSection, base_choice=sec, base_ccobj=comp)
        view.object = choicef

        self.moxx.StubOutWithMock(EditSectionInlineView, 'get_form_kwargs')
        EditSectionInlineView.get_form_kwargs().AndReturn({})
        self.moxx.StubOutWithMock(UpdateWithInlinesView, 'get_form')

        self.moxx.ReplayAll()
        form = view.get_form(ChoiceSectionForm)
        self.moxx.VerifyAll()

        self.assertEqual(type(form), SectionForm)

    def test_edit_section_reget_object(self):
        view = EditSectionInlineView()

        self.moxx.StubOutWithMock(EditSectionInlineView, 'get_object')
        EditSectionInlineView.get_object().AndReturn(None)
        self.moxx.StubOutWithMock(UpdateWithInlinesView, 'construct_inlines')
        UpdateWithInlinesView.construct_inlines().AndReturn(None)

        self.moxx.ReplayAll()
        view.construct_inlines()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_edit_section_get_object(self):
        view = EditSectionInlineView()
        comp = mommy.make(CompendiumClass)
        sec = mommy.make(Section)
        choicef = mommy.make(ChoiceSection, base_choice=sec, base_ccobj=comp)

        self.moxx.StubOutWithMock(EditSectionInlineView, 'get_section')
        EditSectionInlineView.get_section().AndReturn(sec)
        self.moxx.StubOutWithMock(EditSectionInlineView, 'get_compendium_class')
        EditSectionInlineView.get_compendium_class().AndReturn(comp)

        self.moxx.ReplayAll()
        result = view.get_object()
        self.moxx.VerifyAll()

        self.assertEqual(choicef, result)

    def test_edit_section_success_url(self):
        request = RequestFactory()
        view = EditSectionInlineView()
        view.request = request
        view.kwargs = {'cc_id': 0}
        sec = mommy.make(Section)
        view.object = sec

        self.moxx.StubOutWithMock(UpdateWithInlinesView, 'get_success_url')
        UpdateWithInlinesView.get_success_url().AndReturn(None)

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
        ChoiceSection.objects.create(base_ccobj=comp, base_choice=sec)

        self.assertTrue(ChoiceSection.objects.all().exists())

        self.moxx.StubOutWithMock(RemoveSectionView, 'get_compendium_class')
        RemoveSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(RemoveSectionView, 'get_section')
        RemoveSectionView.get_section().AndReturn(sec)

        self.moxx.ReplayAll()
        view.get_redirect_url()
        self.moxx.VerifyAll()

        self.assertFalse(ChoiceSection.objects.all().exists())

    def test_linksection_getsection(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.POST = {'sec_id': 0}
        request.user = user
        view = LinkSectionView()
        view.request = request

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(id=0, user=user).AndReturn(None)

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

        self.assertFalse(ChoiceSection.objects.all().exists())

        self.moxx.StubOutWithMock(LinkSectionView, 'get_compendium_class')
        LinkSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(LinkSectionView, 'get_section')
        LinkSectionView.get_section().AndReturn(sec)

        self.moxx.ReplayAll()
        view.get_redirect_url()
        self.moxx.VerifyAll()

        self.assertTrue(ChoiceSection.objects.all().exists())


class Combined_View_Tests(TestCase):

    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_list_get_queryset(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = ListCombinedClassesView()
        view.request = request

        self.moxx.StubOutWithMock(UserModelManager, 'get_user_objects')
        UserModelManager.get_user_objects(user=user).AndReturn('queryset')
        self.moxx.StubOutWithMock(ListView, 'get_queryset')
        ListView.get_queryset().AndReturn('queryset')

        self.assertFalse(view.queryset)

        self.moxx.ReplayAll()
        result = view.get_queryset()
        self.moxx.VerifyAll()

        self.assertEqual(view.queryset, 'queryset')

    def test_mixin_form_kwargs(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = CreateCombinedClassView()
        view.request = request

        self.moxx.StubOutWithMock(CreateView, 'get_form_kwargs')
        CreateView.get_form_kwargs().AndReturn({})
        self.moxx.StubOutWithMock(UserModelManager, 'get_user_objects')
        UserModelManager.get_user_objects(user=user).AndReturn('queryset')

        self.moxx.ReplayAll()
        result = view.get_form_kwargs()
        self.moxx.VerifyAll()

        self.assertEqual({'user_compendiums': 'queryset'}, result)


    def test_create_combined_class_form_valid(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = CreateCombinedClassView()
        view.request = request
        bine = CombineForm(user_compendiums=[])
        bine.cleaned_data = {'form_name': 'testcc'}

        self.moxx.StubOutWithMock(CreateCombinedClassView, 'get_success_url')
        CreateCombinedClassView.get_success_url().AndReturn(None)

        self.assertFalse(CombinedClass.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=bine)
        self.moxx.VerifyAll()

        self.assertTrue(CombinedClass.objects.all().exists())

    def test_mixin_success_url(self):
        view = EditCombinedClassView()
        view.object = CombinedClass(form_name='testcc', id=99)

        self.moxx.StubOutWithMock(UpdateView, 'get_success_url')
        UpdateView.get_success_url().AndReturn(None)

        self.moxx.ReplayAll()
        view.get_success_url()
        self.moxx.VerifyAll()

        self.assertTrue(view.success_url, "/combinedclasses/99/edit")

    def test_edit_get_object(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = EditCombinedClassView()
        view.request = request
        view.kwargs = {'id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(id=0, user=user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_object()
        self.moxx.VerifyAll()

        # all mocked functions called


class CharacterTests(TestCase):

    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_new_form_kwargs(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = NewCharacterView()
        view.request = request

        self.moxx.StubOutWithMock(FormView, 'get_form_kwargs')
        FormView.get_form_kwargs().AndReturn({})
        self.moxx.StubOutWithMock(NewCharacterView, 'get_object')
        NewCharacterView.get_object().AndReturn('object')

        self.moxx.ReplayAll()
        result = view.get_form_kwargs()
        self.moxx.VerifyAll()

        self.assertEqual({'user': user, 'combined_class': 'object'}, result)

    def test_new_get_obj(self):
        user = User.objects.create(username='testuser')
        request = RequestFactory()
        request.user = user
        view = NewCharacterView()
        view.request = request
        view.kwargs = {'id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(id=0, user=user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_object()
        self.moxx.VerifyAll()

        # all mocked functions called
