from django.contrib.auth import load_backend
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
import mox

from accounts.forms import UsernameLoginForm
from accounts.views import LoginView


class FormTests(TestCase):
    # Precise vailidation error must be detected with coverage

    def setUp(self):
        self.moxx = mox.Mox()
        form = self.form = UsernameLoginForm()
        form.cleaned_data = {'username': 'userfoo', 'password': ''}
        form.user_cache = self.user = User.objects.create(username='userfoo')

    def tearDown(self):
        self.moxx.UnsetStubs()

    def test_authenticate_pass(self):
        self.assertEqual(self.user, self.form.authenticate())

    def test_authenticate_fail(self):
        self.moxx.StubOutWithMock(ModelBackend, 'get_user')
        ModelBackend.get_user(self.user.pk).AndReturn(None)

        self.moxx.ReplayAll()
        user = self.form.authenticate()
        self.moxx.VerifyAll()

        self.assertEqual(user, None)

    def test_clean_success(self):
        self.moxx.StubOutWithMock(self.form, 'authenticate')
        self.form.authenticate().AndReturn(self.user)
        self.moxx.StubOutWithMock(self.form, 'confirm_login_allowed')
        self.form.confirm_login_allowed(self.user).AndReturn(True)

        self.user.backend = True

        self.moxx.ReplayAll()
        self.form.clean()
        self.moxx.VerifyAll()

        # all mocked functions called

    def test_clean_fail(self):
        self.moxx.StubOutWithMock(self.form, 'authenticate')
        self.form.authenticate().AndReturn(self.user)
        self.moxx.StubOutWithMock(self.form, 'confirm_login_allowed')

        self.moxx.ReplayAll()
        self.assertRaises(ImproperlyConfigured, self.form.clean)
        self.moxx.VerifyAll()

    def test_clean_no_user(self):
        # clean_password method will have already thrown a form error
        self.moxx.StubOutWithMock(self.form, 'authenticate')
        self.moxx.StubOutWithMock(self.form, 'confirm_login_allowed')

        self.form.user_cache = None

        self.moxx.ReplayAll()
        self.form.clean()
        self.moxx.VerifyAll()

        # no mocked functions called

    def test_clean_password_with_password(self):
        self.form.cleaned_data['password'] = 'password'
        self.assertRaises(ValidationError, self.form.clean_password)

    def test_clean_password_bad_username(self):
        self.form.cleaned_data['username'] = 'userbar'
        self.assertRaises(ValidationError, self.form.clean_password)

    def test_clean_password_admin_user(self):
        self.user.set_password('password')
        self.user.save()
        self.assertRaises(ValidationError, self.form.clean_password)

    def test_clean_password_success(self):
        self.assertEqual('', self.form.clean_password())


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
