from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
import mox

from accounts.forms import UsernameLoginForm
from accounts.views import LoginView


class ViewTests(TestCase):

    def setUp(self):
        self.moxx = mox.Mox()

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_login(self):
        user = User.objects.create(username='userfoo')
        user.backend = ''
        view = LoginView()
        request = RequestFactory()
        request.META = {}
        request.user = None
        request.session = self.client.session
        request.session.create()
        view.request = request

        form = self.moxx.CreateMock(UsernameLoginForm)
        form.get_user().AndReturn(user)

        self.moxx.ReplayAll()
        view.form_valid(form)
        self.moxx.VerifyAll()

        self.assertTrue(request.user)
