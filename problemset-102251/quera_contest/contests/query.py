from django.contrib.auth import get_user_model
from django.db.models import Max, F, Sum

from problems.models import Submission, Problem
from .models import Contest

User = get_user_model()


def list_problems(contest_id):
    queryset = Problem.objects.filter(contest__id=contest_id).all()
    return queryset


def list_users(contest_id):
    queryset = Contest.objects.get(id=contest_id).participants.all()
    return queryset


def list_submissions(contest_id):
    queryset = (Submission.objects
                .filter(problem__contest=contest_id)
                .order_by('-submitted_time')
                .all()
                )
    return queryset


def list_problem_submissions(contest_id, problem_id):
    queryset = (Submission.objects
                .filter(problem=problem_id, problem__contest=contest_id)
                .order_by('-submitted_time')
                .all()
                )
    return queryset


def list_user_submissions(contest_id, user_id):
    queryset = (Submission.objects
                .filter(participant=user_id, problem__contest=contest_id)
                .order_by('-submitted_time')
                .all()
                )
    return queryset


def list_problem_user_submissions(contest_id, user_id, problem_id):
    queryset = (Submission.objects
                .filter(participant=user_id, problem__contest=contest_id, problem=problem_id)
                .order_by('-submitted_time')
                .all()
                )
    return queryset


def list_users_solved_problem(contest_id, problem_id):
    queryset = (User.objects
                .filter(submissions__problem=problem_id,
                        submissions__problem__contest=contest_id,
                        submissions__score=F('submissions__problem__score'))
                .order_by('-submissions__submitted_time')
                .all())
    return queryset


def user_score(contest_id, user_id):
    final_score = (Submission.objects
                   .filter(problem__contest__id=contest_id, participant_id=user_id)
                   .values('problem_id')
                   .annotate(max_score=Max('score'))
                   .aggregate(final_score=Sum('max_score'))
                   .get('final_score'))

    final_score = 0 if final_score is None else final_score
    return final_score


def list_final_submissions(contest_id):
    queryset = (Submission.objects
                .filter(problem__contest=contest_id)
                .values('participant_id', 'problem_id')
                .annotate(score__max=Max('score'))
                .order_by('participant_id')
                )
    return queryset
