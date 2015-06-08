from django.test import TestCase


# End-To-End test
class Get_Tests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertContains(response, 'Hello Dungeon World')
