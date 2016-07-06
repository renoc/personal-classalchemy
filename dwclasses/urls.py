from django.conf.urls import include, url

import dwclasses.views as views


urlpatterns = [
    url(r'^dwclass/?$',
        views.DWClassListView.as_view()),
    url(r'^dwclass/create',
        views.DWClassCreateView.as_view()),
    url(r'^dwclass/(?P<id>\d+)',
        views.DWClassEditView.as_view()),
    url(r'^preview/(?P<id>\d+)',
        views.DWClassPreView.as_view()),
    url(r'^print/(?P<id>\d+)/?$',
        views.DWClassPreView.as_view(
            template_name='class_create_print.html')),
    url(r'^print/(?P<id>\d+)/levelup',
        views.DWClassPreView.as_view(
            template_name='class_levelup_print.html')),
]
