from django.test import TestCase
from django.urls import reverse

from .question_template import create_question


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """If no question exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Pub_date in the past are displayed on the index page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question])

    def test_future_question(self):
        """Pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Only past questions are displayed."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        resp = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            resp.context['latest_question_list'], [question])

    def test_two_past_question(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(
            question_text="Future question 2.", days=-5)
        resp = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(resp.context['latest_question_list'], [question2, question1],)
