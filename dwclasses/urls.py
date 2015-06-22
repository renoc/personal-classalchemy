from django.conf.urls import include, url

import dwclasses.views as views


urlpatterns = [
    url(r'^compendiumclasses/?$', views.ListCompendiumClassesView.as_view()),
    url(r'^compendiumclasses/create', views.CreateCompendiumClassView.as_view()),
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
    url(r'^combinedclasses/?$', views.ListCombinedClassesView.as_view()),
    url(r'^combinedclasses/create', views.CreateCombinedClassView.as_view()),
    url(r'^combinedclasses/(?P<id>\d+)/edit',
        views.EditCombinedClassView.as_view()),
    url(r'^combinedclasses/(?P<id>\d+)/new_character',
        views.NewCharacterView.as_view()),
]
