from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class SampleTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.other_client = Client()
        self.user = get_user_model().objects.create_user(
            username='quera_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create_user(
            username='other_quera_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create_user(
            username='another_user_quera',
            email='other_test_user@gmail.com',
            password='top_secret'
        )
        self.client.login(username='quera_user', password='top_secret')
        self.other_client.login(username='other_quera_user',
                                password='top_secret')

    def test_get_form_and_prev_funcs(self):
        self.post_empty_response()
        self.post_signup_quera()
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')
        self.assertTrue(
            'Usernames must contain the word "Quera"'.lower() in response.content.decode("utf-8").lower())

    def post_empty_response(self):
        response = self.client.post(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def post_signup_quera(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'another_quera_user',
            'email': 'email@amil.com',
            'password': 'random_pass',
            'confirm_password': 'random_pass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_suggest(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'another+_user:_:quera',
            'email': 'email@amil.com',
            'password': 'random_pass',
            'confirm_password': 'random_pass',
        })
        content = response.content.decode('utf-8').lower()
        self.assertTrue('suggest:' in content)
        s = content.find('*')
        e = content[s + 1:].find('*')

        suggest = content[s + 1:s + e + 1].lower()
        self.assertTrue("Enter a valid username".lower() in content)
        self.assertTrue("quera" in suggest)
        self.assertEquals('another_user_quera_1', suggest)
        self.assertFalse(get_user_model().objects.filter(username=suggest).exists())
