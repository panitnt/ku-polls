import datetime
from django.utils import timezone
from polls.models import Question


def create_question(question_text, days):
    """Create a question"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
