from combinedchoices.models import ChoiceField
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, ModelFormMixin, UpdateView
from django.views.generic.list import ListView

from dwclasses.forms import SectionForm, CompendiumClassForm
from dwclasses.models import CompendiumClass, Section
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
        self.queryset = CompendiumClass.objects.get_user_classes(
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
        ChoiceField.objects.create(
            base_choice=new_obj, base_ccobj=compendium_class)
        return HttpResponseRedirect(self.get_success_url())


class EditSectionView(LoginRequiredMixin, SectionMixin, UpdateView):
    form_class = SectionForm
    template_name = "section_edit.html"

    def get_object(self):
        return self.get_section()

    def get_success_url(self):
        id = self.kwargs.get('cc_id')
        self.success_url = "/compendiumclasses/%s/edit_section/%s" % (
            id, self.object.id)
        return super(EditSectionView, self).get_success_url()


class RemoveSectionView(LoginRequiredMixin, SectionMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        comp = self.get_compendium_class()
        sect = self.get_section()
        ChoiceField.objects.get(base_ccobj=comp, base_choice=sect).delete()
        return "/compendiumclasses/%s" % comp.id


class LinkSectionView(LoginRequiredMixin, SectionMixin, RedirectView):
    permanent = False

    def get_section(self):
        id = self.request.POST.get('sec_id') or 0
        return Section.objects.get_or_404(id=id, user=self.request.user)

    def get_redirect_url(self, *args, **kwargs):
        comp = self.get_compendium_class()
        sect = self.get_section()
        ChoiceField.objects.create(base_ccobj=comp, base_choice=sect)
        return "/compendiumclasses/%s" % comp.id
