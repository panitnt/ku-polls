from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from polls.models import Choice, Question, Vote
import logging


# generic views
class IndexView(generic.ListView):
    """This is IndexView that displays a list of questions.

    Attributes:
        template_name: The name of the template used to render the index.
        context_object_name: The name of the context objects.
    """

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """DetailView can displays a question with a choice.

    Attributes:
        model: Question class.
        template_name: The name of the template used to render to detail.

    Methods:
        get_queryset: Get questions by filter.
        get: Redirect to the question page.
    """

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, pk):
        """Excludes any questions that aren't published yet and except error.

        Args:
            pk: Primary key of Question
        """

        redirect = HttpResponseRedirect(reverse('polls:index'))
        try:
            self.question = get_object_or_404(Question, pk=pk)
        except IndexError:
            messages.error(request, 'Index not found')
            return redirect
        except Http404:
            messages.error(request, 'Http404 not found')
            return redirect
        try:
            self.check_vote = Vote.objects.filter(user=request.user)[0].choice.choice_text
        except IndexError:
            self.check_vote = None
        if not self.question.can_vote():
            messages.error(request, "This question can't vote")
            return redirect
        return render(request, 'polls/detail.html',{'question': self.question, 'check_choice': self.check_vote})
        # return super().get(request, pk=pk)


class ResultsView(generic.DetailView):
    """ResultsView to generate result for each polls.

    Attributes:
        model: Question class.
        template_name: The name of the template used to render to detail.
    """

    model = Question
    template_name = 'polls/results.html'


# same with original
@login_required
def vote(request, question_id):
    """To vote a choice for each question.

    args:
        question_id: Id of this question.
    """
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice"})
    else:
        if not question.can_vote():
            messages.error(request, 'User cannot vote')
            return HttpResponseRedirect(reverse('polls:index'))
        check_vote = Vote.objects.filter(user=request.user, choice__question=question)
        vote = check_vote
        if check_vote.count() == 0:
            vote = Vote(user=user, choice=selected_choice)
        else:
            vote = check_vote[0]
            vote.choice = selected_choice
        vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=[question.id],))


def redirect(self):
    """Redirect to index page."""
    return HttpResponseRedirect(reverse('polls:index'))
