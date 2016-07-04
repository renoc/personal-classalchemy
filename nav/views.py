from django.views.generic.base import RedirectView, TemplateView


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
