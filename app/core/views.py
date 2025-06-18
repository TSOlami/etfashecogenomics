"""
Views for the core app.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Project


def dashboard(request):
    """Main dashboard view - exactly like demo."""
    # For demo, we'll show hardcoded data like the original
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'core/dashboard.html', context)


def analytics_page(request):
    """Analytics page - exactly like demo with tabs."""
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'core/analytics.html', context)


def data_page(request):
    """Data management page - exactly like demo."""
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'core/data.html', context)


def reports_page(request):
    """Reports page - exactly like demo."""
    context = {
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'core/reports.html', context)