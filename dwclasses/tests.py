from django import http
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django import forms
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.edit import (
    CreateView, FormView, FormMixin, UpdateView)
from django.views.generic.list import ListView
from extra_views.advanced import UpdateWithInlinesView
from model_mommy import mommy
import mox

from combinedchoices.models import (
    BaseCCO,
    Choice, ChoiceSection, CompletedCCO, ReadyCCO, Section, UserModelManager)
from config.tests import create_view
from dwclasses import utils
from dwclasses.forms import (
    CompendiumClassForm, SectionForm, ChoiceSectionForm, ChoiceForm,
    CombineForm, NewCharacterForm)
from dwclasses.views import (
    ListCompendiumClassesView, CreateCompendiumClassView,
    EditCompendiumClassView, EditSectionInlineView,
    CreateSectionView, RemoveSectionView, LinkSectionView,
    ListCombinedClassesView, CreateCombinedClassView, EditCombinedClassView,
    NewCharacterView, ViewCharacterView, ListCharacterView)


class Compendium_View_Tests(TestCase):

    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_create_compendium_get_success_url(self):
        view = CreateCompendiumClassView()
        view.object = BaseCCO(form_name='testcc', id=99)
        self.assertTrue(view.get_success_url(), "/compendiumclasses/99")

    def test_create_compendium_class_form_valid(self):
        view = create_view(CreateCompendiumClassView)
        comp = CompendiumClassForm()
        comp.cleaned_data = {'form_name': 'testcc', 'use_dw_defaults': False}

        self.moxx.StubOutWithMock(CompendiumClassForm, 'save')
        CompendiumClassForm.save(commit=False).AndReturn(BaseCCO())
        self.moxx.StubOutWithMock(utils, 'populate_sections')
        self.moxx.StubOutWithMock(CreateCompendiumClassView, 'get_success_url')
        CreateCompendiumClassView.get_success_url().AndReturn(None)
        self.moxx.StubOutWithMock(messages, 'success')
        messages.success(view.request, mox.IsA(unicode)).AndReturn(None)

        self.assertFalse(BaseCCO.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=comp)
        self.moxx.VerifyAll()

        self.assertTrue(BaseCCO.objects.all().exists())

    def test_create_compendium_class_form_populate_trigger(self):
        view = create_view(CreateCompendiumClassView)
        comp = CompendiumClassForm()
        comp.cleaned_data = {'form_name': 'testcc', 'use_dw_defaults': True}
        obj = BaseCCO()

        self.moxx.StubOutWithMock(CompendiumClassForm, 'save')
        CompendiumClassForm.save(commit=False).AndReturn(obj)
        self.moxx.StubOutWithMock(utils, 'populate_sections')
        utils.populate_sections(obj).AndReturn(None)
        self.moxx.StubOutWithMock(CreateCompendiumClassView, 'get_success_url')
        CreateCompendiumClassView.get_success_url().AndReturn(None)
        self.moxx.StubOutWithMock(messages, 'success')
        messages.success(view.request, mox.IsA(unicode)).AndReturn(None)

        self.assertFalse(BaseCCO.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=comp)
        self.moxx.VerifyAll()

        self.assertTrue(BaseCCO.objects.all().exists())

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
        view.request = ''
        view.object = BaseCCO(form_name='testcc', id=99)

        self.moxx.StubOutWithMock(messages, 'success')
        messages.success(view.request, mox.IsA(str)).AndReturn(None)

        self.moxx.ReplayAll()
        url = view.get_success_url()
        self.moxx.VerifyAll()

        self.assertTrue(url, "/compendiumclasses/99")


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
        comp = mommy.make(BaseCCO)
        sec = Section(field_type=0)

        self.moxx.StubOutWithMock(CreateSectionView, 'get_compendium_class')
        CreateSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(SectionForm, 'save')
        SectionForm.save(commit=False).AndReturn(sec)
        self.moxx.StubOutWithMock(CreateSectionView, 'get_success_url')
        CreateSectionView.get_success_url().AndReturn(None)
        self.moxx.StubOutWithMock(messages, 'success')
        messages.success(view.request, mox.IsA(unicode)).AndReturn(None)

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
        comp = mommy.make(BaseCCO)
        sec = mommy.make(Section)
        choicef = mommy.make(ChoiceSection, section=sec, basecco=comp)
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
        comp = mommy.make(BaseCCO)
        sec = mommy.make(Section)
        choicef = mommy.make(ChoiceSection, section=sec, basecco=comp)

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
        self.moxx.StubOutWithMock(messages, 'success')
        messages.success(view.request, mox.IsA(unicode)).AndReturn(None)

        self.moxx.ReplayAll()
        view.get_success_url()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_remove_section(self):
        view = create_view(RemoveSectionView)
        comp = mommy.make(BaseCCO)
        sec = mommy.make(Section)
        ChoiceSection.objects.create(basecco=comp, section=sec)

        self.assertTrue(ChoiceSection.objects.all().exists())

        self.moxx.StubOutWithMock(RemoveSectionView, 'get_compendium_class')
        RemoveSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(RemoveSectionView, 'get_section')
        RemoveSectionView.get_section().AndReturn(sec)
        self.moxx.StubOutWithMock(messages, 'warning')
        messages.warning(view.request, mox.IsA(unicode)).AndReturn(None)

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
        comp = mommy.make(BaseCCO)
        sec = mommy.make(Section)

        self.assertFalse(ChoiceSection.objects.all().exists())

        self.moxx.StubOutWithMock(LinkSectionView, 'get_compendium_class')
        LinkSectionView.get_compendium_class().AndReturn(comp)
        self.moxx.StubOutWithMock(LinkSectionView, 'get_section')
        LinkSectionView.get_section().AndReturn(sec)
        self.moxx.StubOutWithMock(messages, 'success')
        messages.success(view.request, mox.IsA(unicode)).AndReturn(None)

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

        self.assertFalse(ReadyCCO.objects.all().exists())

        self.moxx.ReplayAll()
        view.form_valid(form=bine)
        self.moxx.VerifyAll()

        self.assertTrue(ReadyCCO.objects.all().exists())

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

        self.assertEqual(
            {'ready_obj': 'object', 'user': view.request.user}, result)

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

    def test_character_form_valid(self):
        view = create_view(NewCharacterView)
        combined = mommy.make(ReadyCCO)
        kwargs = {'ready_obj':combined, 'user':None}

        self.moxx.StubOutWithMock(NewCharacterView, 'get_success_url')
        NewCharacterView.get_success_url().AndReturn('/')
        self.moxx.StubOutWithMock(NewCharacterView, 'get_form_kwargs')
        self.moxx.StubOutWithMock(http, 'HttpResponseRedirect')
        http.HttpResponseRedirect('/').AndReturn(None)
        self.moxx.StubOutWithMock(NewCharacterForm, 'save')
        NewCharacterForm.save().AndReturn(None)
        self.moxx.StubOutWithMock(NewCharacterForm, 'create_section_field')

        self.moxx.ReplayAll()
        form = NewCharacterForm(**kwargs)
        view.form_valid(form=form)
        self.moxx.VerifyAll()

        # proper mocked functions called

    def test_create_character_get_success_url(self):
        view = NewCharacterView()
        view.object = CompletedCCO(form_name='testcc', id=99)
        self.assertTrue(view.get_success_url(), "/characters/99")


class Utility_Tests(TestCase):

    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_get_section_true(self):
        sect = Section.objects.create(field_name='Adventurer Gear', field_type=0)
        result = utils.get_section(('gear', 'Gear', {}),)
        self.assertEqual(result, sect)

    def test_get_section_false(self):
        sect = Section.objects.create(field_name='Equipment', field_type=0)
        result = utils.get_section(('gear', 'Gear', {'field_type': 0}),)
        self.assertNotEqual(result, sect)

    def test_populate_sections_basic(self):
        comp = BaseCCO.objects.create()
        section = ['gear', 'Gear', {'field_type': 0}]
        sect = Section.objects.create(field_type=0)

        self.moxx.StubOutWithMock(utils, 'get_section')
        utils.get_section(section, user=None).AndReturn(sect)

        self.assertFalse(comp.choicesection_set.exists())

        self.moxx.ReplayAll()
        utils.populate_sections(comp, [section])
        self.moxx.VerifyAll()

        self.assertTrue(comp.choicesection_set.exists())
        self.assertFalse(Choice.objects.all().exists())

    def test_populate_sections_advanced(self):
        comp = BaseCCO.objects.create()
        section = ['2-5', 'Advanced Moves 2-5', {'field_type': 0}]
        sect = Section.objects.create(
            field_name='Advanced Moves 2-5', field_type=0)

        self.moxx.StubOutWithMock(utils, 'get_section')
        utils.get_section(section, user=None).AndReturn(sect)

        self.assertFalse(comp.choicesection_set.exists())

        self.moxx.ReplayAll()
        utils.populate_sections(comp, [section])
        self.moxx.VerifyAll()

        self.assertTrue(comp.choicesection_set.exists())
        self.assertTrue(Choice.objects.all().exists())

    def test_populate_sections_advanceder(self):
        comp = BaseCCO.objects.create()
        section = ['6-10', 'Advanced Moves 6-10', {'field_type': 0}]
        sect = Section.objects.create(
            field_name='Advanced Moves 6-10', field_type=0)

        self.moxx.StubOutWithMock(utils, 'get_section')
        utils.get_section(section, user=None).AndReturn(sect)

        self.assertFalse(comp.choicesection_set.exists())

        self.moxx.ReplayAll()
        utils.populate_sections(comp, [section])
        self.moxx.VerifyAll()

        self.assertTrue(comp.choicesection_set.exists())
        self.assertTrue(Choice.objects.all().exists())
