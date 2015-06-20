from combinedchoices.models import Choice, ChoiceField
from django.forms import widgets
from django.forms.models import ModelForm
from extra_views import InlineFormSet

from dwclasses.models import CompendiumClass, CombinedClass, Section


class ChoiceForm(InlineFormSet):
    model = Choice


class CompendiumClassForm(ModelForm):
    class Meta:
        model = CompendiumClass
        exclude = ('user',)


class SectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ('user',)


class ChoiceSectionForm(ModelForm):
    class Meta:
        model = Choice
        exclude = []


class CombineForm(ModelForm):
    class Meta:
        model = CombinedClass
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        user_compendiums = kwargs.pop('user_compendiums')
        super(CombineForm, self).__init__(*args, **kwargs)
        self.fields['included_forms'].widget = widgets.CheckboxSelectMultiple(
            choices=self.fields['included_forms'].choices)
        self.fields["included_forms"].queryset = user_compendiums
