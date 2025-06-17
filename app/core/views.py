"""
Views for the core app.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project


@login_required
def dashboard(request):
    """Main dashboard view."""
    recent_projects = Project.objects.filter(
        models.Q(owner=request.user) | models.Q(collaborators=request.user)
    ).distinct()[:5]
    
    context = {
        'recent_projects': recent_projects,
        'user': request.user,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def projects_page(request):
    """Projects listing page."""
    projects = Project.objects.filter(
        models.Q(owner=request.user) | models.Q(collaborators=request.user)
    ).distinct()
    
    context = {
        'projects': projects,
    }
    return render(request, 'core/projects.html', context)


@login_required
def project_detail(request, project_id):
    """Project detail page."""
    project = get_object_or_404(
        Project,
        id=project_id,
        models.Q(owner=request.user) | models.Q(collaborators=request.user)
    )
    
    context = {
        'project': project,
    }
    return render(request, 'core/project_detail.html', context)