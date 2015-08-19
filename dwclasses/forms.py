from django.forms.fields import BooleanField, CharField

from combinedchoices.forms import BaseCCOForm, ReadyForm


class CompendiumClassForm(BaseCCOForm):
    use_dw_defaults = BooleanField(
        label='Populate with DungeonWorld Data', initial=True, required=False)


class NewCharacterForm(ReadyForm):
    form_name = CharField(label='Character Name')
