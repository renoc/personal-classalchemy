from django.contrib import admin

from combinedchoices.admin import BaseCCObjAdmin
from dwclasses.models import Section, CompendiumClass


class CompendiumClassAdmin(BaseCCObjAdmin):
    model = CompendiumClass


class SectionAdmin(BaseCCObjAdmin):
    model = Section
    list_display = ['field_name', 'user']


admin.site.register(Section, SectionAdmin)
admin.site.register(CompendiumClass, CompendiumClassAdmin)
