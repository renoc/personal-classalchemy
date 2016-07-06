from django.forms.models import ModelForm

from dwclasses.models import DWClass


class DWClassForm(ModelForm):
    class Meta:
        model = DWClass
        exclude = ['user']
