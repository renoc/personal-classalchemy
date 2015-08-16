from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

from combinedchoices.models import BaseCCObj, BaseChoice, UserModelMixin


class Section(UserModelMixin, BaseChoice):

    def validate_unique(self, exclude=None):
        # Call parent class to bypass override on parent class
        super(BaseChoice, self).validate_unique(exclude=exclude)
        duplicates = Section.objects.exclude(id=self.id).filter(
            field_name=self.field_name, user=self.user)
        if duplicates.exists():
            ValidationError(('Non-Unique Name Error'), code='invalid')

    def __unicode__(self):
        if not self.user:
            return super(Section, self).__unicode__()
        else:
            return '%s - %s' % (self.user.username, self.field_name)


class CompendiumClass(UserModelMixin, BaseCCObj):

    def __unicode__(self):
        if not self.user:
            return super(CompendiumClass, self).__unicode__()
        else:
            return '%s - %s' % (self.user.username, self.form_name)

    @property
    def name(self):
        return self.form_name

    def available_sections(self):
        return Section.objects.filter(user=self.user).exclude(
            compendiumclass=self)
