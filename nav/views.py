from django.shortcuts import render
from django.views.generic.base import TemplateView


class About (TemplateView):
    template_name = 'about.html'


class Home (TemplateView):
    template_name = 'home.html'
