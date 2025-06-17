"""
Views for the core app.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Project


@login_required
def dashboard(request):
    """Main dashboard view - matches demo dashboard."""
    recent_projects = Project.objects.filter(
        models.Q(owner=request.user) | models.Q(collaborators=request.user)
    ).distinct()[:5]
    
    context = {
        'recent_projects': recent_projects,
        'user': request.user,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def analytics_page(request):
    """Analytics page - matches demo analytics with tabs."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/analytics.html', context)


@login_required
def data_page(request):
    """Data management page - matches demo data section."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/data.html', context)


@login_required
def reports_page(request):
    """Reports page - matches demo reports section."""
    context = {
        'user': request.user,
    }
    return render(request, 'core/reports.html', context)