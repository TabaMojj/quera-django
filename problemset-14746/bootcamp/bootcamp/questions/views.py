import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse_lazy

from bootcamp.activities.models import Activity
from bootcamp.decorators import ajax_required
from bootcamp.questions.forms import AnswerForm, QuestionForm
from bootcamp.questions.models import Answer, Question, Comment


@login_required
def _questions(request, questions, active):
    paginator = Paginator(questions, 10)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)

    except PageNotAnInteger:
        questions = paginator.page(1)

    except EmptyPage:  # pragma: no cover
        questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/questions.html', {
        'questions': questions,
        'active': active
    })


class AskQuestion(LoginRequiredMixin, CreateView):
    """
    """
    template_name = 'questions/ask.html'
    form_class = QuestionForm
    success_url = reverse_lazy('questions')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AskQuestion, self).form_valid(form)


@login_required
def questions(request):
    return unanswered(request)


@login_required
def answered(request):
    questions = Question.get_answered()
    return _questions(request, questions, 'answered')


@login_required
def unanswered(request):
    questions = Question.get_unanswered()
    return _questions(request, questions, 'unanswered')


@login_required
def all(request):
    questions = Question.objects.all()
    return _questions(request, questions, 'all')


@login_required
def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    comments = question.comments.all()
    form = AnswerForm(initial={'question': question})
    return render(request, 'questions/question.html', {
        'question': question,
        'comments': comments,
        'form': form
    })


@login_required
def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            answer = Answer()
            answer.user = request.user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            user.profile.notify_answered(answer.question)
            return redirect('/questions/{0}/'.format(answer.question.pk))

        else:
            question = form.cleaned_data.get('question')
            return render(request, 'questions/question.html', {
                'question': question,
                'form': form
            })

    else:
        return redirect('/questions/')


@login_required
@ajax_required
def accept(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    user = request.user
    try:
        # answer.accept cleans previous accepted answer
        user.profile.unotify_accepted(answer.question.get_accepted_answer())

    except Exception:
        pass

    if answer.question.user == user:
        answer.accept()
        user.profile.notify_accepted(answer)
        return HttpResponse()

    else:
        return HttpResponseForbidden()


@login_required
@ajax_required
def vote(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(
        Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE),  # noqa: E501
        user=user, answer=answer_id)
    if activity:
        activity.delete()

    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        activity = Activity(activity_type=vote, user=user, answer=answer_id)
        activity.save()

    return HttpResponse(answer.calculate_votes())


@login_required
@ajax_required
def question_vote(request):
    question_id = request.POST['question']
    question = Question.objects.get(pk=question_id)
    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(
        Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE),  # noqa: E501
        user=user, question=question_id)
    if activity:
        activity.delete()

    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        activity = Activity(activity_type=vote,
                            user=user, question=question_id)
        activity.save()

    return HttpResponse(question.calculate_votes())


@login_required
@ajax_required
def favorite(request):
    question_id = request.POST['question']
    question = Question.objects.get(pk=question_id)
    user = request.user
    activity = Activity.objects.filter(activity_type=Activity.FAVORITE,
                                       user=user, question=question_id)
    if activity:
        activity.delete()
        user.profile.unotify_favorited(question)

    else:
        activity = Activity(activity_type=Activity.FAVORITE, user=user,
                            question=question_id)
        activity.save()
        user.profile.notify_favorited(question)

    return HttpResponse(question.calculate_favorites())


@login_required
@ajax_required
def comment(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status': 3}), content_type="application/json")

    question_id = request.POST.get('question')
    comment_text = request.POST.get('comment')
    if question_id is None:
        return HttpResponseBadRequest('`question` not available in request.')
    if comment_text is None:
        return HttpResponseBadRequest('`comment` not available in request.')

    if not comment_text or comment_text.isspace():
        return HttpResponse(json.dumps({'status': 1}), content_type="application/json")

    question_object = Question.objects.filter(id=question_id)
    if not question_object.exists():
        return HttpResponse(json.dumps({'status': 2}), content_type="application/json")
    user = User.objects.get(username=request.user.username)
    Comment.objects.create(question=question_object.get(), user=user, text=comment_text)
    return HttpResponse(json.dumps({'status': 0}), content_type="application/json")
