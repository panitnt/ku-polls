from django.test import TestCase
from django.urls import reverse
from .question_template import create_question


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """In the future return error message and return to index page."""
        future_ques = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_ques.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """Question with a pub_date in the past displays the question text."""
        past_ques = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_ques.id,))
        response = self.client.get(url)
        self.assertContains(response, past_ques.question_text)
