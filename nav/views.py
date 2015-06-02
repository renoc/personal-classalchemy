from django.shortcuts import render
from django.views.generic.base import TemplateView

class Home (TemplateView):
    template_name = 'nav/home.html'
