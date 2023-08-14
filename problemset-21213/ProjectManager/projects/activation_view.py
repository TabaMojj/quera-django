from django.shortcuts import redirect, get_object_or_404

from .models import ProjectMembership


def active_project(request, project_id):
    project_membership = get_object_or_404(ProjectMembership, project_id=project_id, user=request.user)
    ProjectMembership.objects.filter(user=request.user).update(is_current=False)
    project_membership.is_current = True
    project_membership.save()
    return redirect('index')
