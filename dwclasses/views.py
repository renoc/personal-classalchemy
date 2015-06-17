from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from dwclasses.forms import CompendiumClassForm
from dwclasses.models import CompendiumClass
from nav.models import LoginRequiredMixin


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
        new_class = form.save(commit=False)
        new_class.user = user=self.request.user
        new_class.save()
        self.object = new_class
        return HttpResponseRedirect(self.get_success_url())


class EditCompendiumClassView(LoginRequiredMixin, UpdateView):
    form_class = CompendiumClassForm
    template_name = "compendium_class_edit.html"

    def get_object(self):
        id = self.kwargs.get('id')
        return CompendiumClass.objects.get_or_404(
            id=id, user=self.request.user)

    def get_success_url(self):
        # Super call prevents DRYing
        id = self.object.id
        self.success_url = "/compendiumclasses/%s" % id
        return super(EditCompendiumClassView, self).get_success_url()
