from django.conf.urls import include, url

import dwclasses.views as views


urlpatterns = [
    url(r'^compendiumclasses/create', views.CreateCompendiumClassView.as_view()),
    url(r'^compendiumclasses/?$', views.ListCompendiumClassesView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/?$',
        views.EditCompendiumClassView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/create_section',
        views.CreateSectionView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/edit_section/(?P<sec_id>\d+)',
        views.EditSectionInlineView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/remove_section/(?P<sec_id>\d+)',
        views.RemoveSectionView.as_view()),
    url(r'^compendiumclasses/(?P<cc_id>\d+)/link_section',
        views.LinkSectionView.as_view()),
]
