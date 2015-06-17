from django.forms.models import ModelForm

from dwclasses.models import CompendiumClass


class CompendiumClassForm(ModelForm):
    class Meta:
        model = CompendiumClass
        fields = ('form_name',)
