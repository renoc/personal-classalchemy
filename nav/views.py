from django.views.generic.base import TemplateView


class About (TemplateView):
    template_name = 'about.html'


class BaseCharacterSheet (TemplateView):
    template_name = 'basecharacter_print.html'


class Home (TemplateView):
    template_name = 'home.html'


class PAQ (TemplateView):
    template_name = 'paq.html'
