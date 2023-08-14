from django.contrib.auth.models import User
from django.db import models, transaction


class Project(models.Model):
    name = models.CharField(max_length=100)


class ProjectMembership(models.Model):
    ROLE_GUEST = 'RG'
    ROLE_REPORTER = 'RR'
    ROLE_DEVELOPER = 'RD'
    ROLE_MASTER = 'RM'
    ROLE_OWNER = 'RO'

    ROLE_CHOICES = (
        (ROLE_GUEST, 'Guest'),
        (ROLE_REPORTER, 'Reporter'),
        (ROLE_DEVELOPER, 'Developer'),
        (ROLE_MASTER, 'Master'),
        (ROLE_OWNER, 'Owner'),

    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=ROLE_CHOICES, default=ROLE_GUEST, verbose_name='Role')
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'project')


