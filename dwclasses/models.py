from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404


class UserModelManager(models.QuerySet):

    def filter_user_objects(self, user):
        return self.filter(user=user)

    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)


class UserModelMixin(models.Model):
    SELF_FILTER = ['user']
    user = models.ForeignKey(User, null=True, blank=True)
    objects = UserModelManager.as_manager()

    class Meta:
        abstract = True

    def self_kwargs(self):
        kwargs = {}
        for selfilter in self.SELF_FILTER:
            kwargs.update({selfilter: getattr(self, selfilter, None)})
        return kwargs

    def unicode_prefex(self):
        if self.user:
            return '%s - ' % self.user
        else:
            return ''


ModelMixin = UserModelMixin


class DWClass(ModelMixin):
    class_name = models.CharField(max_length=64, null=False, blank=False)
    tagline = models.CharField(
        max_length=512, null=False, blank=True, default='')
    stats = models.TextField(null=False, blank=True, default='')
    quest = models.TextField(null=False, blank=True, default='')
    drive = models.TextField(null=False, blank=True, default='')
    aspect = models.TextField(null=False, blank=True, default='')
    bonds = models.TextField(null=False, blank=True, default='')
    gear = models.TextField(null=False, blank=True, default='')
    # picture
    starting_left = models.TextField(null=False, blank=True, default='')
    starting_right = models.TextField(null=False, blank=True, default='')
    advanced_low = models.TextField(null=False, blank=True, default='')
    advanced_high = models.TextField(null=False, blank=True, default='')

    def __unicode__(self):
        return '%s%s' % (self.unicode_prefex(), self.class_name)

    def validate_unique(self, exclude=None):
        super(DWClass, self).validate_unique(exclude=exclude)
        duplicates = type(self).objects.exclude(id=self.id).filter(
            class_name=self.class_name, **self.self_kwargs())
        if duplicates.exists():
            raise ValidationError(('Non-Unique Name Error'), code='invalid')
