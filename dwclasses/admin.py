from django.contrib import admin
from combinedchoices.admin import (
    BaseCCObjAdmin, ChoiceSectionAdmin, ChoiceAdmin)
from dwclasses.models import (
    Section, CompendiumClass, CombinedClass, CompendiumSection, Selection)


class CompendiumClassAdmin(BaseCCObjAdmin):
    model = CompendiumClass


class SectionAdmin(BaseCCObjAdmin):
    model = Section
    list_display = ['field_name', 'user']


class SelectionAdmin(ChoiceAdmin):
    model = Selection


class CompendiumSectionAdmin(ChoiceSectionAdmin):
    model = CompendiumSection
    inlines = [SelectionAdmin,]


admin.site.register(Section, SectionAdmin)
admin.site.register(CompendiumClass, CompendiumClassAdmin)
admin.site.register(CompendiumSection, CompendiumSectionAdmin)
admin.site.register(CombinedClass)
