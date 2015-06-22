from django.contrib import admin
from combinedchoices.admin import (
    BaseCCObjAdmin, ChoiceSection, ChoiceSectionAdmin)
from dwclasses.models import (
    Section, CompendiumClass, CompletedCharacter, CombinedClass)


class CompendiumClassAdmin(BaseCCObjAdmin):
    model = CompendiumClass


admin.site.register(Section)
admin.site.register(CompendiumClass, CompendiumClassAdmin)
#admin.site.register(ChoiceSection, ChoiceSectionAdmin)
admin.site.register(CompletedCharacter)
admin.site.register(CombinedClass)
