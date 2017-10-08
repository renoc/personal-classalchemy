from django import http
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from dwclasses.forms import DWClassForm
from dwclasses.models import DWClass
from nav.models import LoginRequiredMixin


class UserModelMixin(object):

    def get_object(self):
        id = self.kwargs.get('id')
        return self.model.objects.get_or_404(id=id, user=self.request.user)

    def get_queryset(self):
        self.queryset = self.model.objects.filter_user_objects(
            self.request.user)
        return super(UserModelMixin, self).get_queryset()


class DWClassMixin(LoginRequiredMixin, UserModelMixin, object):
    model = DWClass
    form_class = DWClassForm
    template_name = "class_edit.html"

    def get_success_url(self):
        messages.success(
            self.request, '%s Class Updated.' % self.object.class_name)
        self.success_url = "/dwclass/%s" % self.object.id
        return super(DWClassMixin, self).get_success_url()


class DWClassCreateView(DWClassMixin, CreateView):

    def form_valid(self, form):
        new_obj = form.save(commit=False)
        new_obj.user = user = self.request.user
        new_obj.save()
        self.object = new_obj
        return http.HttpResponseRedirect(self.get_success_url())


class DWClassEditView(DWClassMixin, UpdateView):
    pass


class DWClassListView(LoginRequiredMixin, UserModelMixin, ListView):
    model = DWClass
    template_name = "class_list.html"


class DWClassPreView(LoginRequiredMixin, UserModelMixin, DetailView):
    model = DWClass
    template_name = "preview.html"


class PreviewListView(LoginRequiredMixin, UserModelMixin, ListView):
    model = DWClass
    template_name = "preview_list.html"
