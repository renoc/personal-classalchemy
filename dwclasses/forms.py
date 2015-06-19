from django.forms.models import ModelForm

from dwclasses.models import CompendiumClass, Section


class CompendiumClassForm(ModelForm):
    class Meta:
        model = CompendiumClass
        fields = ('form_name',)


class SectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ('user',)
