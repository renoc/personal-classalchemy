from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic.edit import CreateView, UpdateView
import mox

from models import DWClass, UserModelManager
from views import DWClassCreateView


class BasicModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.get_or_create(username='bob')[0]

    def test_unicode_no_user(self):
        name = 'new mod'
        mod = DWClass(class_name=name)
        self.assertEqual('%s' % mod, name)

    def test_unicode_with_user(self):
        name = 'new mod'
        mod = DWClass(class_name=name, user=self.user)
        self.assertEqual('%s' % mod, 'bob - %s' % name)

    def test_filter_user_objects(self):
        mod = DWClass.objects.get_or_create(user=self.user)[0]
        DWClass.objects.create()
        self.assertEqual(
            DWClass.objects.filter_user_objects(user=self.user).get().id,
            mod.id)

    def test_404(self):
        self.assertRaises(Http404, DWClass.objects.get_or_404, id=0)

    def test_self_filter(self):
        mod = DWClass.objects.get_or_create(user=self.user)[0]
        self.assertEqual(mod.self_kwargs()['user'], self.user)


class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.get_or_create(username='bob')[0]
        mod = self.mod = DWClass.objects.get_or_create(
            user=self.user, class_name='Developer')[0]
        request = self.request = RequestFactory()
        request.user = self.user
        view = self.view = DWClassCreateView(kwargs={'id':mod.id})
        view.object = mod
        view.request = request
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_mixin_get_object(self):
        self.moxx.StubOutWithMock(UserModelManager, 'get_or_404')
        UserModelManager.get_or_404(
            id=self.mod.id, user=self.user).AndReturn('object')

        self.moxx.ReplayAll()
        self.view.get_object()
        self.moxx.VerifyAll()

    def test_mixin_get_queryset(self):
        self.moxx.StubOutWithMock(UserModelManager, 'filter_user_objects')
        UserModelManager.filter_user_objects(self.user).AndReturn('object')
        self.moxx.StubOutWithMock(CreateView, 'get_queryset')
        CreateView.get_queryset().AndReturn('pass')

        self.assertEqual(self.view.queryset, None)
        self.moxx.ReplayAll()
        self.view.get_queryset()
        self.moxx.VerifyAll()
        self.assertEqual(self.view.queryset, 'object')

    def test_dwmixin_get_success_url(self):
        self.moxx.StubOutWithMock(CreateView, 'get_success_url')
        CreateView.get_success_url().AndReturn('pass')
        self.moxx.StubOutWithMock(messages, 'success')
        messages.success(self.request, 'Developer Class Updated.')

        self.assertEqual(self.view.success_url, None)
        self.moxx.ReplayAll()
        self.view.get_success_url()
        self.moxx.VerifyAll()
        self.assertEqual(self.view.success_url, '/dwclass/1')
