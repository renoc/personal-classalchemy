from django.conf.urls import include, url

import dwclasses.views as views


urlpatterns = [
    url(r'^compendiumclasses/create', views.CreateCompendiumClassView.as_view()),
    url(r'^compendiumclasses/?$', views.ListCompendiumClassesView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/?$',
        views.EditCompendiumClassView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/create_section',
        views.CreateClassSectionView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/edit_section/(?P<sec_id>\d+)',
        views.EditClassSectionView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/remove_section/(?P<sec_id>\d+)',
        views.RemoveClassSectionView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/link_section',
        views.LinkClassSectionView.as_view()),
]
