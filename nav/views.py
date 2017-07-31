from django.contrib import messages
from django.views.generic.base import RedirectView, TemplateView

from suggestionbox.views import EditSuggestionView


class About (TemplateView):
    template_name = 'about.html'


class BaseCharacterPreview (TemplateView):
    template_name = 'basecharacter_preview.html'


class BaseCharacterPrint (TemplateView):
    template_name = 'basecharacter_print.html'


class Home (TemplateView):
    template_name = 'home.html'


class PAQ (RedirectView):
    permanent = True
    url = '/about'


class SuggestionView(EditSuggestionView):
    success_url = '/feedback'
    template_name = "feedback.html"

    def get_success_url(self):
        messages.success(self.request, 'Feedback Sent')
        return super(SuggestionView, self).get_success_url()
