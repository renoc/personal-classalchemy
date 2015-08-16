from combinedchoices.models import CompletedCCO
from django import http
from django.contrib import messages
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, FormView, ModelFormMixin, UpdateView)
from django.views.generic.list import ListView
from extra_views.advanced import UpdateWithInlinesView

from combinedchoices.models import Choice
from dwclasses import utils
from dwclasses.forms import (
    ChoiceForm, CompendiumSectionForm, CombineForm, CompendiumClassForm,
    SectionForm, NewCharacterForm)
from dwclasses.models import (
    CombinedClass, CompendiumClass, Section, CompendiumSection)
from nav.models import LoginRequiredMixin


class SectionMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ModelFormMixin, self).get_context_data(**kwargs)
        context['compendium_class'] = self.get_compendium_class()
        return context

    def get_compendium_class(self):
        id = self.kwargs.get('cc_id')
        return CompendiumClass.objects.get_or_404(id=id, user=self.request.user)

    def get_section(self):
        id = self.kwargs.get('sec_id')
        return Section.objects.get_or_404(id=id, user=self.request.user)


class UserModelMixin(object):

    def get_object(self):
        id = self.kwargs.get('id')
        return self.model.objects.get_or_404(
            id=id, user=self.request.user)

    def get_queryset(self):
        self.queryset = self.model.objects.get_user_objects(
            user=self.request.user)
        return super(UserModelMixin, self).get_queryset()


class ListCompendiumClassesView(LoginRequiredMixin, UserModelMixin, ListView):
    model = CompendiumClass
    template_name = "compendium_class_list.html"


class CreateCompendiumClassView(LoginRequiredMixin, CreateView):
    form_class = CompendiumClassForm
    template_name = "compendium_class_create.html"

    def get_success_url(self):
        id = self.object.id
        self.success_url = "/compendiumclasses/%s" % id
        return super(CreateCompendiumClassView, self).get_success_url()

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.user = self.request.user
        new_obj.save()
        self.object = new_obj
        messages.success(
            self.request, '%s Class Created.' % new_obj.form_name)
        if form.cleaned_data['use_dw_defaults']:
            utils.populate_sections(new_obj)
        return http.HttpResponseRedirect(self.get_success_url())


class EditCompendiumClassView(LoginRequiredMixin, SectionMixin, UpdateView):
    form_class = CompendiumClassForm
    template_name = "compendium_class_edit.html"

    def get_object(self):
        return self.get_compendium_class()

    def get_success_url(self):
        messages.success(
            self.request, '%s Class Updated.' % self.object.form_name)
        id = self.object.id
        self.success_url = "/compendiumclasses/%s" % id
        return super(EditCompendiumClassView, self).get_success_url()


class CreateSectionView(LoginRequiredMixin, SectionMixin, CreateView):
    form_class = SectionForm
    template_name = "section_create.html"

    def get_success_url(self):
        id = self.kwargs.get('cc_id')
        self.success_url = "/compendiumclasses/%s/edit_section/%s" % (
            id, self.object.id)
        return super(CreateSectionView, self).get_success_url()

    def form_valid(self, form):
        compendium_class = self.get_compendium_class()
        new_obj = form.save(commit=False)
        new_obj.user = user=self.request.user
        new_obj.save()
        messages.success(
            self.request, '%s Section Created.' % new_obj.field_name)
        self.object = new_obj
        CompendiumSection.objects.create(
            base_choice=new_obj, base_ccobj=compendium_class)
        return http.HttpResponseRedirect(self.get_success_url())


class EditSectionInlineView(LoginRequiredMixin, SectionMixin,
                            UpdateWithInlinesView):
    form_class = CompendiumSectionForm
    inlines = [ChoiceForm]
    inline_model = Choice
    model = CompendiumSection
    template_name = "section_edit.html"

    def get_form(self, form_class):
        if not form_class == CompendiumSectionForm:
            return super(EditSectionInlineView, self).get_form(form_class)
        kwargs = self.get_form_kwargs()
        kwargs['instance'] = self.object.base_choice
        return SectionForm(**kwargs)

    def construct_inlines(self):
        # undo form_valid change
        self.object = self.get_object()
        return super(EditSectionInlineView, self).construct_inlines()

    def get_object(self):
        return CompendiumSection.objects.get(
            base_choice=self.get_section(),
            base_ccobj=self.get_compendium_class())

    def get_success_url(self):
        messages.success(
            self.request, '%s Section Updated.' % self.object.field_name)
        id = self.kwargs.get('cc_id')
        self.success_url = "/compendiumclasses/%s/edit_section/%s" % (
            id, self.object.id)
        return super(EditSectionInlineView, self).get_success_url()


class RemoveSectionView(LoginRequiredMixin, SectionMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        comp = self.get_compendium_class()
        sect = self.get_section()
        messages.warning(
            self.request, '%s Section Removed!' % sect.field_name)
        CompendiumSection.objects.get(base_ccobj=comp, base_choice=sect).delete()
        return "/compendiumclasses/%s" % comp.id


class LinkSectionView(LoginRequiredMixin, SectionMixin, RedirectView):
    permanent = False

    def get_section(self):
        id = self.request.POST.get('sec_id') or 0
        return Section.objects.get_or_404(id=id, user=self.request.user)

    def get_redirect_url(self, *args, **kwargs):
        comp = self.get_compendium_class()
        sect = self.get_section()
        messages.success(
            self.request, '%s Section Added.' % sect.field_name)
        CompendiumSection.objects.create(base_ccobj=comp, base_choice=sect)
        return "/compendiumclasses/%s" % comp.id


class ListCombinedClassesView(LoginRequiredMixin, UserModelMixin, ListView):
    model = CombinedClass
    template_name = "combined_class_list.html"


class CombinedMixin(object):
    form_class = CombineForm
    success_url = "/combinedclasses"

    def get_form_kwargs(self):
        kwargs = super(CombinedMixin, self).get_form_kwargs()
        kwargs['user_compendiums'] = CompendiumClass.objects.get_user_objects(
            user=self.request.user)
        return kwargs


class CreateCombinedClassView(LoginRequiredMixin, CombinedMixin, CreateView):
    template_name = "combined_class_create.html"

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.user = user=self.request.user
        new_obj.save()
        form.save_m2m()
        self.object = new_obj
        return http.HttpResponseRedirect(self.get_success_url())


class EditCombinedClassView(LoginRequiredMixin, CombinedMixin, UserModelMixin,
                            UpdateView):
    model = CombinedClass
    template_name = "combined_class_create.html"


class NewCharacterView(LoginRequiredMixin, UserModelMixin, FormView):
    form_class = NewCharacterForm
    model = CombinedClass
    template_name = "character_new.html"

    def form_valid(self, form):
        self.object = form.save()
        return http.HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(NewCharacterView, self).get_form_kwargs()
        kwargs['ready_class'] = self.get_object()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        self.success_url = "/characters/%s" % self.object.id
        return super(FormView, self).get_success_url()


class ViewCharacterView(LoginRequiredMixin, UserModelMixin, DetailView):
    model = CompletedCCO
    template_name = "character_view.html"


class ListCharacterView(LoginRequiredMixin, UserModelMixin, ListView):
    model = CompletedCCO
    template_name = "character_list.html"
