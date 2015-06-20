from combinedchoices.models import Choice, ChoiceField
from django.forms.models import ModelForm
from extra_views import InlineFormSet

from dwclasses.models import CompendiumClass, Section


class ChoiceForm(InlineFormSet):
    model = Choice


class CompendiumClassForm(ModelForm):
    class Meta:
        model = CompendiumClass
        fields = ('form_name',)


class SectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ('user',)


class ChoiceSectionForm(ModelForm):
    class Meta:
        model = Choice
        exclude = []
