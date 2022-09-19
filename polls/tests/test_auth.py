import datetime
from urllib import response
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .question_template import create_question

class QuestionAuthTest(TestCase):
    def setUp(self) -> None:
        self.register = reverse('register')
        self.user1 = {
            'email' : 'isp1@gmail.com',
            'username' : 'isp-1',
            'password' : 'isp1-test',
            'first_name' : 'Ant'
        }
        self.user2 = {
            'email' : 'isp2@gmail.com',
            'username' : 'isp-2',
            'password' : 'isp2-test',
            'first_name' : 'Bird'
        }
        self.user3 = {
            'email' : 'isp3@gmail.com',
            'username' : 'isp-3',
            'password' : 'isp3-test',
            'first_name' : 'Cat'
        }
    def test_can_access_auth(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

