from django.conf import settings
from django.db import models


class Problem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=100)


class Submission(models.Model):
    submitted_time = models.DateTimeField()
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submissions', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="submissions", on_delete=models.CASCADE)
    code = models.URLField(max_length=200)
    score = models.PositiveIntegerField(default=0)
