from functools import wraps

from django.http import HttpResponseNotFound, HttpResponseForbidden

from .models import ProjectMembership


# noinspection PyPep8Naming
class projects_panel(object):
    def __init__(self, permissions=None):
        self.permissions = permissions

    def __call__(self, view_func):

        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            memberships = ProjectMembership.objects.filter(user=request.user)
            if memberships:
                request.memberships = memberships
            else:
                return HttpResponseNotFound('No projects found')

            current_membership = memberships.filter(is_current=True)
            if not current_membership:
                current_membership = memberships.earliest('id')
                current_membership.is_current = True
                current_membership.save()
            else:
                current_membership = current_membership.earliest('id')

            request.current_membership = current_membership
            request.project = current_membership.project

            if self.permissions:
                for permission in self.permissions:
                    if not request.current_membership.has_permission(permission):
                        return HttpResponseForbidden()

            return view_func(request, *args, **kwargs)

        return _wrapper_view
