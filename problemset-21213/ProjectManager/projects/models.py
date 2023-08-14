from django.contrib.auth.models import User
from django.db import models


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

    PERMISSIONS = {
        'create_new_issue': [ROLE_GUEST, ROLE_REPORTER, ROLE_DEVELOPER, ROLE_MASTER, ROLE_OWNER],
        'leave_comments': [ROLE_GUEST, ROLE_REPORTER, ROLE_DEVELOPER, ROLE_MASTER, ROLE_OWNER],
        'pull_project_code': [ROLE_REPORTER, ROLE_DEVELOPER, ROLE_MASTER, ROLE_OWNER],
        'assign_issues_and_merge_requests': [ROLE_REPORTER, ROLE_DEVELOPER, ROLE_MASTER, ROLE_OWNER],
        'see_a_list_of_merge_requests': [ROLE_REPORTER, ROLE_DEVELOPER, ROLE_MASTER, ROLE_OWNER],
        'manage_merge_requests': [ROLE_DEVELOPER, ROLE_MASTER, ROLE_OWNER],
        'create_new_branches': [ROLE_DEVELOPER, ROLE_MASTER, ROLE_OWNER],
        'add_new_team_members': [ROLE_MASTER, ROLE_OWNER],
        'push_to_protected_branches': [ROLE_MASTER, ROLE_OWNER],
        'switch_visibility_level': [ROLE_OWNER],
        'remove_project': [ROLE_OWNER],
        'force_push_to_protected_branches': [],
    }

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=ROLE_CHOICES, default=ROLE_GUEST, verbose_name='Role')
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'project')

    def has_permission(self, action):
        if self.role in self.PERMISSIONS.get(action, []):
            return True
        return False

