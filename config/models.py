from django.shortcuts import get_object_or_404


class ManagerMixin(object):

    def get_user_objects(self, user):
        return self.filter(user=user)

    def get_or_404(self, *args, **kwargs):
        return get_object_or_404(self.model, *args, **kwargs)
