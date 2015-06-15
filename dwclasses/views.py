from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from dwclasses.models import CompendiumClass
from nav.models import LoginRequiredMixin


class ListCompendiumClassesView(LoginRequiredMixin, ListView):
    model = CompendiumClass
    template_name = "list_compendium_classes.html"

    def get_queryset(self):
        self.queryset = CompendiumClass.objects.get_list(user=self.request.user)
        return super(ListCompendiumClassesView, self).get_queryset()
