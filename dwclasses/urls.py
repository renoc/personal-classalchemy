from django.conf.urls import include, url

import dwclasses.views as views


urlpatterns = [
    url(r'^compendiumclasses/create', views.CreateCompendiumClassView.as_view()),
    url(r'^compendiumclasses/?$', views.ListCompendiumClassesView.as_view()),
    url(r'^compendiumclasses/(?P<id>\d+)/?$', views.EditCompendiumClassView.as_view()),
]
