from django.conf.urls import include, url

import dwclasses.views as views


urlpatterns = [
    url(r'^compendiumclasses/?$', views.ListCompendiumClassesView.as_view()),
]
