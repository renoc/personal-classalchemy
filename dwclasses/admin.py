from django.contrib import admin
from combinedchoices.admin import (
    BaseCCObjAdmin, ChoiceField, ChoiceFieldAdmin)
from dwclasses.models import (
    ClassChoice, CompendiumClass, CompletedCharacter, CombinedClass)


class CompendiumClassAdmin(BaseCCObjAdmin):
    model = CompendiumClass


admin.site.register(ClassChoice)
admin.site.register(CompendiumClass, CompendiumClassAdmin)
#admin.site.register(ChoiceField, ChoiceFieldAdmin)
admin.site.register(CompletedCharacter)
admin.site.register(CombinedClass)
