from combinedchoices.models import ChoiceSection, Choice
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
from config.tests import create_view
from dwclasses.forms import (
    CompendiumClassForm, SectionForm, ChoiceSectionForm, ChoiceForm,
    CombineForm, NewCharacterForm)
from dwclasses.models import (
    CombinedClass, CompendiumClass, CompletedCharacter, Section)
from dwclasses.views import (
    ListCompendiumClassesView, CreateCompendiumClassView,
    EditCompendiumClassView, CreateSectionView, EditSectionInlineView,
    RemoveSectionView, LinkSectionView, ListCombinedClassesView,
    CreateCombinedClassView, EditCombinedClassView, NewCharacterView,
    ViewCharacterView, ListCharacterView)


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

    def test_create_compendium_get_success_url(self):
        view = CreateCompendiumClassView()
        view.object = CompendiumClass(form_name='testcc', id=99)
        self.assertTrue(view.get_success_url(), "/compendiumclasses/99")

    def test_create_compendium_class_form_valid(self):
        view = create_view(CreateCompendiumClassView)
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
        view = create_view(EditCompendiumClassView)
        view.kwargs = {'cc_id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(
            id=0, user=view.request.user).AndReturn(None)

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
        view = create_view(EditSectionInlineView)
        view.kwargs = {'cc_id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(
            id=0, user=view.request.user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_compendium_class()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_mixin_get_section(self):
        view = create_view(EditSectionInlineView)
        view.kwargs = {'sec_id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(
            id=0, user=view.request.user).AndReturn(None)

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
        view = create_view(CreateSectionView)
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
        view = create_view(EditSectionInlineView)
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
        view = create_view(RemoveSectionView)
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
        view = create_view(LinkSectionView)
        view.request.POST = {'sec_id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(
            id=0, user=view.request.user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_section()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_link_existing_section(self):
        view = create_view(LinkSectionView)
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

    def test_list_mixin_get_queryset(self):
        view = create_view(ListCombinedClassesView)

        self.moxx.StubOutWithMock(UserModelManager, 'get_user_objects')
        UserModelManager.get_user_objects(
            user=view.request.user).AndReturn('queryset')
        self.moxx.StubOutWithMock(ListView, 'get_queryset')
        ListView.get_queryset().AndReturn('queryset')

        self.assertFalse(view.queryset)

        self.moxx.ReplayAll()
        result = view.get_queryset()
        self.moxx.VerifyAll()

        self.assertEqual(view.queryset, 'queryset')

    def test_mixin_form_kwargs(self):
        view = create_view(CreateCombinedClassView)

        self.moxx.StubOutWithMock(CreateView, 'get_form_kwargs')
        CreateView.get_form_kwargs().AndReturn({})
        self.moxx.StubOutWithMock(UserModelManager, 'get_user_objects')
        UserModelManager.get_user_objects(
            user=view.request.user).AndReturn('queryset')

        self.moxx.ReplayAll()
        result = view.get_form_kwargs()
        self.moxx.VerifyAll()

        self.assertEqual({'user_compendiums': 'queryset'}, result)


    def test_create_combined_class_form_valid(self):
        view = create_view(CreateCombinedClassView)
        bine = CombineForm(user_compendiums=[])
        bine.cleaned_data = {'form_name': 'testcc'}

        self.moxx.StubOutWithMock(CreateCombinedClassView, 'get_success_url')
        CreateCombinedClassView.get_success_url().AndReturn(None)

        self.assertFalse(CombinedClass.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=bine)
        self.moxx.VerifyAll()

        self.assertTrue(CombinedClass.objects.all().exists())

    def test_mixin_get_object(self):
        view = create_view(EditCombinedClassView)
        view.kwargs = {'id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(
            id=0, user=view.request.user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_object()
        self.moxx.VerifyAll()

        # all mocked functions called


class Character_View_Tests(TestCase):

    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_new_form_kwargs(self):
        view = create_view(NewCharacterView)

        self.moxx.StubOutWithMock(FormView, 'get_form_kwargs')
        FormView.get_form_kwargs().AndReturn({})
        self.moxx.StubOutWithMock(NewCharacterView, 'get_object')
        NewCharacterView.get_object().AndReturn('object')

        self.moxx.ReplayAll()
        result = view.get_form_kwargs()
        self.moxx.VerifyAll()

        self.assertEqual({'combined_class': 'object'}, result)

    def test_new_get_obj(self):
        view = create_view(NewCharacterView)
        view.kwargs = {'id': 0}

        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(
            id=0, user=view.request.user).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_object()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_character_form_init(self):
        section = mommy.make(Section, field_name='test_section')
        compendium = mommy.make(CompendiumClass, form_name='test_compendium')
        cs = mommy.make(
            ChoiceSection, base_ccobj=compendium, base_choice=section)
        choice = mommy.make(Choice, text='test_choice', choice_section=cs)
        combined = mommy.make(
            CombinedClass, included_forms=[compendium])
        form = NewCharacterForm(combined_class=combined)
        self.assertEqual(
            form.fields['test_section'].widget.choices[0][1], 'test_choice')

    def test_character_form_valid(self):
        view = create_view(NewCharacterView)
        choice = mommy.make(Choice, text='steak')
        combined = mommy.make(
            CombinedClass, included_forms=[choice.choice_section.base_ccobj])
        kwargs = {'combined_class':combined}
        form = NewCharacterForm(**kwargs)
        form.cleaned_data = {'form_name': 'testcc', 'entree': [choice]}

        self.moxx.StubOutWithMock(NewCharacterView, 'get_success_url')
        NewCharacterView.get_success_url().AndReturn('/')
        self.moxx.StubOutWithMock(NewCharacterView, 'get_form_kwargs')
        NewCharacterView.get_form_kwargs().AndReturn(kwargs)

        self.assertFalse(CompletedCharacter.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=form)
        self.moxx.VerifyAll()

        self.assertTrue(CompletedCharacter.objects.all().exists())

    def test_create_character_get_success_url(self):
        view = NewCharacterView()
        view.object = CompletedCharacter(form_name='testcc', id=99)
        self.assertTrue(view.get_success_url(), "/characters/99")
