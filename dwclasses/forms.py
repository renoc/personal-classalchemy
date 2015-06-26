from django.forms.fields import BooleanField, CharField
from django.forms.forms import Form
from django.forms.models import ModelForm, ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from extra_views import InlineFormSet

from dwclasses.models import (
    CompletedCharacter, CompendiumClass, CombinedClass, Section,
    CompendiumSection, Selection)


class ChoiceChoice(ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return obj.text


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


class NewCharacterForm(Form):
    form_name = CharField(label='Character Name')

    def __init__(self, *args, **kwargs):
        combined_class = kwargs.pop('combined_class')
        user = combined_class.user
        super(NewCharacterForm, self).__init__(*args, **kwargs)
        compendiums = combined_class.included_forms.filter(user=user)
        for section in self.get_sections(combined_class, compendiums):
            queryset = Selection.objects.filter(
                choice_section__base_ccobj__in=compendiums,
                choice_section__base_choice=section).order_by('text')
            self.fields[section.field_name] = ChoiceChoice(queryset=queryset,
                help_text=section.instructions)
            self.fields[section.field_name].label = section.field_name
            self.fields[section.field_name].widget = CheckboxSelectMultiple(
                choices=self.fields[section.field_name].choices)

    def get_sections(self, combined_class, compendiums):
        return Section.objects.filter(
            compendiumsection__base_ccobj__in=compendiums,
            user=combined_class.user)

    def save(self, *args, **kwargs):
        combined_class = kwargs.pop('combined_class')
        user = combined_class.user
        character = {}
        name = self.cleaned_data.pop('form_name')
        for section in self.cleaned_data.keys():
            character[section] = []
            for choice in self.cleaned_data[section]:
                character[section].append(choice.text)
        return CompletedCharacter.objects.create(
            form_name=name, form_data=character, user=user)
