import datetime
from urllib import response
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_is_published_with_recent_question(self):
        """is_published() returns True if current date is on or after question publication date."""
        time = timezone.localtime()
        now_question = Question(pub_date=time - datetime.timedelta(hours=23))
        self.assertIs(now_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published() returns False if current date is on or before question publication date."""
        time = timezone.localtime()
        future_question = Question(pub_date=time + datetime.timedelta(days=30))
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_on_recently_question(self):
        """returns True if voting is allowed for recently question."""
        time = timezone.localtime()
        recently_question = Question(
            pub_date=time - datetime.timedelta(days=15), end_date=time + datetime.timedelta(days=30))
        self.assertIs(recently_question.can_vote(), True)

    def test_can_vote_on_future_question(self):
        """returns False if voting is allowed for future question."""
        time = timezone.localtime()
        future_question = Question(pub_date=time + datetime.timedelta(days=30))
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_on_recently_question_but_after_end_date(self):
        """returns False if voting is allowed for recently question but after end date."""
        time = timezone.localtime()
        question = Question(pub_date=time - datetime.timedelta(days=30), end_date=time - datetime.timedelta(days=15))
        self.assertIs(question.can_vote(), False)
    
    def test_can_vote_on_recently_question_no_end_date(self):
        """returns True if voting is allowed for recently question with no end date."""
        time = timezone.localtime()
        question = Question(pub_date=time - datetime.timedelta(days=30))
        self.assertIs(question.can_vote(), True)
    def test_can_vote_on_now_question(self):
        """"""
        time = timezone.localtime()
        now_question = Question(pub_date=time)
        self.assertIs(now_question.can_vote(), True)


def create_question(question_text, days):
    """Create a question with the given `question_text` and published the given number of `days` offset to now (negative for questions published in the past, positive for question that have yet to be published)."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """If no question exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Question with a pub_date in the past are displayed on the index page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question])

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question])

    def test_two_past_question(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(
            question_text="Future question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1],)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future return error message and return back to index page."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
