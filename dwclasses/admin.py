from django.contrib import admin

from combinedchoices.admin import (
    BaseCCObjAdmin, ChoiceSectionAdmin, ChoiceAdmin)
from dwclasses.models import Section, CompendiumClass, CompendiumSection


class CompendiumClassAdmin(BaseCCObjAdmin):
    model = CompendiumClass


class SectionAdmin(BaseCCObjAdmin):
    model = Section
    list_display = ['field_name', 'user']


class CompendiumSectionAdmin(ChoiceSectionAdmin):
    model = CompendiumSection
    inlines = [ChoiceAdmin,]


admin.site.register(Section, SectionAdmin)
admin.site.register(CompendiumClass, CompendiumClassAdmin)
admin.site.register(CompendiumSection, CompendiumSectionAdmin)
