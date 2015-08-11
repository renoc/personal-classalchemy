from django.forms.fields import BooleanField, CharField
from django.forms.forms import Form
from django.forms.models import (
    ModelForm, ModelChoiceField, ModelMultipleChoiceField)
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect, Textarea
from extra_views import InlineFormSet

from combinedchoices.forms import ReadyForm
from dwclasses.models import (
    CompletedCharacter, CompendiumClass, CombinedClass, Section,
    CompendiumSection, Selection)


class ChoiceForm(InlineFormSet):
    model = Selection


class CompendiumClassForm(ModelForm):
    use_dw_defaults = BooleanField(
        label='Populate with DungeonWorld Data', initial=True, required=False)

    class Meta:
        model = CompendiumClass
        fields = ('form_name',)


class SectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ('user',)


class CompendiumSectionForm(ModelForm):
    class Meta:
        model = Selection
        exclude = []


class CombineForm(ModelForm):
    class Meta:
        model = CombinedClass
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        user_compendiums = kwargs.pop('user_compendiums')
        super(CombineForm, self).__init__(*args, **kwargs)
        self.fields['included_forms'].widget = CheckboxSelectMultiple(
            choices=self.fields['included_forms'].choices)
        self.fields['included_forms'].queryset = user_compendiums


class NewCharacterForm(ReadyForm):
    form_name = CharField(label='Character Name')

    def __init__(self, *args, **kwargs):
        self.user = user = kwargs.pop('user')
        super(NewCharacterForm, self).__init__(
            *args, filters={'user':user}, **kwargs)

    def save(self, *args, **kwargs):
        return super(NewCharacterForm, self).save(user=self.user)
