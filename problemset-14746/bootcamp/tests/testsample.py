import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

import os
import django
from django.conf import settings
from django.test.utils import get_runner, teardown_test_environment, setup_test_environment

from bootcamp.questions.models import *


class SampleTest(TestCase):
    def previous_functionality(self):
        teardown_test_environment()
        os.environ['DJANGO_SETTINGS_MODULE'] = 'bootcamp.settings'
        django.setup()
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(['bootcamp.questions'])
        setup_test_environment()
        self.assertFalse(bool(failures))

    def test_question_comment_and_past_functionalities(self):
        self.previous_functionality()

        user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        other_user = get_user_model().objects.create_user(
            username='other_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        question_one = Question.objects.create(
            user=user, title='This is a sample question',
            description='This is a sample question description',
            tags='test1,test2')
        question_two = Question.objects.create(
            user=user,
            title='A Short Title',
            description='''This is a really good content, just if somebody
                            published it, that would be awesome, but no, nobody wants to
                            publish it, because they know this is just a test, and you
                            know than nobody wants to publish a test, just a test;
                            everybody always wants the real deal.''',
            favorites=0,
            has_accepted_answer=True
        )
        answer = Answer.objects.create(
            user=user,
            question=question_two,
            description='A reaaaaally loooong content',
            votes=0,
            is_accepted=True
        )
        c = Client()
        c.force_login(other_user)
        response = c.get('/questions/1/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('This is a sample question' in str(response.context['question']))
        self.assertTrue('test_user' == str(response.context['question'].user))

        response = c.post('/questions/question/comment/', {'question': 1, 'comment': 'in yek comment ast'},
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content.decode('utf-8')).get('status'), 0)
        response = c.get('/questions/1/')
        self.assertTrue('in yek comment ast' in str(response.content.decode('utf-8')))

    def test_question_bad_comment(self):
        self.previous_functionality()

        user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        other_user = get_user_model().objects.create_user(
            username='other_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        question_one = Question.objects.create(
            user=user, title='This is a sample question',
            description='This is a sample question description',
            tags='test1,test2')
        question_two = Question.objects.create(
            user=user,
            title='A Short Title',
            description='''This is a really good content, just if somebody
                            published it, that would be awesome, but no, nobody wants to
                            publish it, because they know this is just a test, and you
                            know than nobody wants to publish a test, just a test;
                            everybody always wants the real deal.''',
            favorites=0,
            has_accepted_answer=True
        )
        answer = Answer.objects.create(
            user=user,
            question=question_two,
            description='A reaaaaally loooong content',
            votes=0,
            is_accepted=True
        )
        c = Client()
        response = c.post('/questions/question/comment/', {'question': 1, 'comment': 'in yek comment ast!111'},
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        c.force_login(other_user)
        response = c.get('/questions/1/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse('in yek comment ast!111' in str(response.content.decode('utf-8')))

        self.assertTrue('This is a sample question' in str(response.context['question']))
        self.assertTrue('test_user' == str(response.context['question'].user))

        response = c.post('/questions/question/comment/', {'question': 1, 'comment': ''},
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode('utf-8')).get('status'), 1)
