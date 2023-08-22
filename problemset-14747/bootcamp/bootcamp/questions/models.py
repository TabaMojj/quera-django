from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import markdown
from bootcamp.activities.models import Activity
from taggit.managers import TaggableManager


@python_2_unicode_compatible
class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    has_accepted_answer = models.BooleanField(default=False)
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-update_date',)

    def __str__(self):
        return self.title

    @staticmethod
    def get_unanswered():
        return Question.objects.filter(has_accepted_answer=False)

    @staticmethod
    def get_answered():
        return Question.objects.filter(has_accepted_answer=True)

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def get_accepted_answer(self):
        return Answer.objects.get(question=self, is_accepted=True)

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')

    def get_description_preview(self):
        if len(self.description) > 255:
            return '{0}...'.format(self.description[:255])

        else:
            return self.description

    def get_description_preview_as_markdown(self):
        return markdown.markdown(self.get_description_preview(),
                                 safe_mode='escape')

    def calculate_favorites(self):
        favorites = Activity.objects.filter(activity_type=Activity.FAVORITE,
                                            question=self.pk).count()
        self.favorites = favorites
        self.save()
        return self.favorites

    def get_favoriters(self):
        favorites = Activity.objects.filter(activity_type=Activity.FAVORITE,
                                            question=self.pk)
        return [favorite for favorite in favorites]

    def calculate_votes(self):
        up_votes = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                           question=self.pk).count()
        down_votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                             question=self.pk).count()
        self.votes = up_votes - down_votes
        self.save()
        return self.votes

    def get_up_voters(self):
        votes = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                        question=self.pk)
        return [vote for vote in votes]

    def get_down_voters(self):
        votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                        question=self.pk)
        return [vote for vote in votes]


@python_2_unicode_compatible
class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    votes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('-is_accepted', '-votes', 'create_date',)

    def __str__(self):
        return self.description

    def accept(self):
        answers = Answer.objects.filter(question=self.question)
        for answer in answers:
            answer.is_accepted = False
            answer.save()
        self.is_accepted = True
        self.save()
        self.question.has_accepted_answer = True
        self.question.save()

    def calculate_votes(self):
        up_votes = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                           answer=self.pk).count()
        down_votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                             answer=self.pk).count()
        self.votes = up_votes - down_votes
        self.save()
        return self.votes

    def get_up_voters(self):
        votes = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                        answer=self.pk)
        return [vote for vote in votes]

    def get_down_voters(self):
        votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                        answer=self.pk)
        return [vote for vote in votes]

    def get_description_as_markdown(self):
        return markdown.markdown(self.description, safe_mode='escape')
