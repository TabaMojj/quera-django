from django.shortcuts import redirect

from projects.models import Project, ProjectMembership


def active_project(request, project_id):

    return redirect('index')
