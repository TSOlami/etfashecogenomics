"""
Views for the core app.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
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
        id=project_id
    )
    
    # Check if user has access to this project
    if not (project.owner == request.user or request.user in project.collaborators.all()):
        from django.http import Http404
        raise Http404("Project not found")
    
    context = {
        'project': project,
    }
    return render(request, 'core/project_detail.html', context)


@login_required
def analytics_page(request):
    """Analytics page."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/analytics.html', context)


@login_required
def data_page(request):
    """Data management page."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/data.html', context)


@login_required
def reports_page(request):
    """Reports page."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/reports.html', context)


@login_required
def sample_tracking_page(request):
    """Sample tracking page."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/sample_tracking.html', context)


@login_required
def quality_control_page(request):
    """Quality control page."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/quality_control.html', context)