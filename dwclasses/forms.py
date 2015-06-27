from django.forms.fields import BooleanField, CharField
from django.forms.forms import Form
from django.forms.models import (
    ModelForm, ModelChoiceField, ModelMultipleChoiceField)
from django.forms.widgets import CheckboxSelectMultiple, Textarea
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
        for section in self.get_sections(user, compendiums):
            if section.cross_combine:
                name = section.field_name
                queryset = Selection.objects.filter(
                    choice_section__base_ccobj__in=compendiums)
                self.create_section_field(name, section, queryset)
            else:
                for compendium in compendiums:
                    name = '%s - %s' % (
                        compendium.form_name, section.field_name)
                    queryset = Selection.objects.filter(
                        choice_section__base_ccobj=compendium)
                    self.create_section_field(name, section, queryset)

    def create_section_field(self, name, section, queryset):
        queryset = queryset.filter(
            choice_section__base_choice=section).order_by('text')
        if section.field_type is Section.TEXT:
            self.fields[name] = CharField(
                help_text=section.instructions, required=False,
                initial='\n\n'.join(queryset.values_list('text', flat=True)))
            self.fields[name].widget = Textarea()
            self.fields[name].widget.attrs.update(
                {'class':'combo-text', 'read-only':True})
        else:
            self.fields[name] = ChoiceChoice(
                queryset=queryset, help_text=section.instructions)
            self.fields[name].widget = CheckboxSelectMultiple(
                choices=self.fields[name].choices)
        self.fields[name].label = name

    def get_sections(self, user, compendiums):
        return Section.objects.filter(
            compendiumsection__base_ccobj__in=compendiums, user=user)

    def save(self, *args, **kwargs):
        combined_class = kwargs.pop('combined_class')
        user = combined_class.user
        character = {}
        name = self.cleaned_data.pop('form_name')
        for section in self.cleaned_data.keys():
            character[section] = []
            data = self.cleaned_data[section]
            if type(data) == unicode:
                character[section].append(data)
            else:
                for choice in self.cleaned_data[section]:
                    character[section].append(choice.text)
        return CompletedCharacter.objects.create(
            form_name=name, form_data=character, user=user)
