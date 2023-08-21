from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from order_food.models import Food


class TestComment(TestCase):
    def setUp(self):
        self.f1 = Food.objects.create(name='GhormeSabzi', description='Khoresht', price=15000)
        self.f2 = Food.objects.create(name='Soltani', description='Kabab', price=23000)

    def test_check_form_not_singed_in(self):
        c = Client()
        response = c.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'GhormeSabzi')
        self.assertContains(response, 'Khoresht')
        self.assertContains(response, 'Soltani')
        self.assertContains(response, 'Kabab')
        self.assertContains(response, '15000')
        self.assertContains(response, '23000')

        self.assertNotContains(response, '<form')
        self.assertNotContains(response, '</form>')
        self.assertNotContains(response, 'your comment successfully submitted')
        self.assertContains(response, 'Please log in to leave a comment.')
