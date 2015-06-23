from combinedchoices.models import Choice, ChoiceSection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, FormView, ModelFormMixin, UpdateView)
from django.views.generic.list import ListView
from extra_views.advanced import UpdateWithInlinesView

from dwclasses.forms import (
    ChoiceForm, ChoiceSectionForm, CombineForm, CompendiumClassForm,
    SectionForm, NewCharacterForm)
from dwclasses.models import (
    CompendiumClass, CompletedCharacter, Section, CombinedClass)
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


class ListCompendiumClassesView(LoginRequiredMixin, ListView):
    model = CompendiumClass
    template_name = "compendium_class_list.html"

    def get_queryset(self):
        self.queryset = CompendiumClass.objects.get_user_objects(
            user=self.request.user)
        return super(ListCompendiumClassesView, self).get_queryset()


class CreateCompendiumClassView(LoginRequiredMixin, CreateView):
    form_class = CompendiumClassForm
    template_name = "compendium_class_create.html"

    def get_success_url(self):
        id = self.object.id
        self.success_url = "/compendiumclasses/%s" % id
        return super(CreateCompendiumClassView, self).get_success_url()

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.user = user=self.request.user
        new_obj.save()
        self.object = new_obj
        return HttpResponseRedirect(self.get_success_url())


class EditCompendiumClassView(LoginRequiredMixin, SectionMixin, UpdateView):
    form_class = CompendiumClassForm
    template_name = "compendium_class_edit.html"

    def get_object(self):
        return self.get_compendium_class()

    def get_success_url(self):
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
        self.object = new_obj
        ChoiceSection.objects.create(
            base_choice=new_obj, base_ccobj=compendium_class)
        return HttpResponseRedirect(self.get_success_url())


class EditSectionInlineView(LoginRequiredMixin, SectionMixin,
                            UpdateWithInlinesView):
    form_class = ChoiceSectionForm
    inlines = [ChoiceForm]
    inline_model = Choice
    model = ChoiceSection
    template_name = "section_edit.html"

    def get_form(self, form_class):
        if not form_class == ChoiceSectionForm:
            return super(EditSectionInlineView, self).get_form(form_class)
        kwargs = self.get_form_kwargs()
        kwargs['instance'] = self.object.base_choice.section
        return SectionForm(**kwargs)

    def construct_inlines(self):
        # undo form_valid change
        self.object = self.get_object()
        return super(EditSectionInlineView, self).construct_inlines()

    def get_object(self):
        return ChoiceSection.objects.get(
            base_choice=self.get_section(),
            base_ccobj=self.get_compendium_class())

    def get_success_url(self):
        id = self.kwargs.get('cc_id')
        self.success_url = "/compendiumclasses/%s/edit_section/%s" % (
            id, self.object.id)
        return super(EditSectionInlineView, self).get_success_url()


class RemoveSectionView(LoginRequiredMixin, SectionMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        comp = self.get_compendium_class()
        sect = self.get_section()
        ChoiceSection.objects.get(base_ccobj=comp, base_choice=sect).delete()
        return "/compendiumclasses/%s" % comp.id


class LinkSectionView(LoginRequiredMixin, SectionMixin, RedirectView):
    permanent = False

    def get_section(self):
        id = self.request.POST.get('sec_id') or 0
        return Section.objects.get_or_404(id=id, user=self.request.user)

    def get_redirect_url(self, *args, **kwargs):
        comp = self.get_compendium_class()
        sect = self.get_section()
        ChoiceSection.objects.create(base_ccobj=comp, base_choice=sect)
        return "/compendiumclasses/%s" % comp.id


class ListCombinedClassesView(LoginRequiredMixin, ListView):
    model = CombinedClass
    template_name = "combined_class_list.html"

    def get_queryset(self):
        self.queryset = CombinedClass.objects.get_user_objects(
            user=self.request.user)
        return super(ListCombinedClassesView, self).get_queryset()


class CombinedMixin(object):
    form_class = CombineForm

    def get_form_kwargs(self):
        kwargs = super(CombinedMixin, self).get_form_kwargs()
        kwargs['user_compendiums'] = CompendiumClass.objects.get_user_objects(
            user=self.request.user)
        return kwargs

    def get_success_url(self):
        self.success_url = "/combinedclasses/%s/edit" % self.object.id
        return super(CombinedMixin, self).get_success_url()


class CreateCombinedClassView(LoginRequiredMixin, CombinedMixin, CreateView):
    template_name = "combined_class_create.html"

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.user = user=self.request.user
        new_obj.save()
        form.save_m2m()
        self.object = new_obj
        return HttpResponseRedirect(self.get_success_url())


class EditCombinedClassView(LoginRequiredMixin, CombinedMixin, UpdateView):
    template_name = "combined_class_create.html"

    def get_object(self):
        id = self.kwargs.get('id')
        return CombinedClass.objects.get_or_404(id=id, user=self.request.user)


class NewCharacterView(LoginRequiredMixin, FormView):
    form_class = NewCharacterForm
    template_name = "character_new.html"

    def form_valid(self, form):
        self.object = form.save(**self.get_form_kwargs())
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(NewCharacterView, self).get_form_kwargs()
        kwargs['combined_class'] = self.get_object()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self):
        id = self.kwargs.get('id')
        return CombinedClass.objects.get_or_404(id=id, user=self.request.user)

    def get_success_url(self):
        self.success_url = "/characters/%s" % self.object.id
        return super(FormView, self).get_success_url()


class ViewCharacterView(LoginRequiredMixin, DetailView):
    template_name = "character_view.html"

    def get_object(self):
        id = self.kwargs.get('id')
        return CompletedCharacter.objects.get_or_404(
            id=id, user=self.request.user)


class ListCharacterView(LoginRequiredMixin, ListView):
    model = CompletedCharacter
    template_name = "character_list.html"

    def get_queryset(self):
        self.queryset = CompletedCharacter.objects.get_user_objects(
            user=self.request.user)
        return super(ListCharacterView, self).get_queryset()
