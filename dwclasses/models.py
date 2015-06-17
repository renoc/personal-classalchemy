from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

from config.models import ManagerMixin
from combinedchoices.models import (
    BaseCCObj, BaseChoice, CompletedCombinedObj, ReadyCombinedObj)


class ClassChoice(BaseChoice):
    user = models.ForeignKey(User, null=True, blank=True)

    def validate_unique(self, exclude=None):
        # Call parent class to bypass override on parent class
        super(BaseChoice, self).validate_unique(exclude=exclude)
        duplicates = ClassChoice.objects.exclude(id=self.id).filter(
            field_name=self.field_name, user=self.user)
        if duplicates.exists():
            ValidationError(('Non-Unique Name Error'),
                            code='invalid')

    def __unicode__(self):
        if not self.user:
            return super(ClassChoice, self).__unicode__()
        else:
            return '%s - %s' % (self.user.username, self.field_name)


class CombinedClass(ReadyCombinedObj):
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        if not self.user:
            return super(CombinedClass, self).__unicode__()
        else:
            return '%s - %s' % (self.user.username, self.form_name)


class CompendiumClassManager(ManagerMixin, models.QuerySet):
    def get_user_classes(self, user):
        return self.filter(user=user)


class CompendiumClass(BaseCCObj):
    user = models.ForeignKey(User, null=True, blank=True)
    objects = CompendiumClassManager.as_manager()

    def __unicode__(self):
        if not self.user:
            return super(CompendiumClass, self).__unicode__()
        else:
            return '%s - %s' % (self.user.username, self.form_name)

    @property
    def name(self):
        return self.form_name


class CompletedCharacter(CompletedCombinedObj):
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        if not self.user:
            return super(CompletedCharacter, self).__unicode__()
        else:
            return '%s - %s' % (self.user.username, self.form_name)
