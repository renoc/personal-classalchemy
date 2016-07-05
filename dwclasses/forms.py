from django.forms.fields import BooleanField, CharField
from django.forms.models import ModelForm

from combinedchoices.forms import BaseCCOForm, ReadyForm
from dwclasses.models import DWClass


class CompendiumClassForm(BaseCCOForm):
    use_dw_defaults = BooleanField(
        label='Populate with DungeonWorld Data', initial=True, required=False)


class DWClassForm(ModelForm):
    class Meta:
        model = DWClass
        exclude = ['user']


class NewCharacterForm(ReadyForm):
    form_name = CharField(label='Character Name')
