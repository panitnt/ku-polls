import datetime
from django.test import TestCase
from django.utils import timezone

from polls.models import Question


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
