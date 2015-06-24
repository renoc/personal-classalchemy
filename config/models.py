from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class UserModelManager(models.QuerySet):

    def get_user_objects(self, user):
        return self.filter(user=user)

    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)


class UserModelMixin(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    objects = UserModelManager.as_manager()

    class Meta:
        abstract = True
