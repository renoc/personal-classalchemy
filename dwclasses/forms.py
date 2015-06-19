from django.forms.models import ModelForm

from dwclasses.models import CompendiumClass, ClassChoice


class CompendiumClassForm(ModelForm):
    class Meta:
        model = CompendiumClass
        fields = ('form_name',)


class ClassSectionForm(ModelForm):
    class Meta:
        model = ClassChoice
        exclude = ('user',)
