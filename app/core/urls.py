"""
URL configuration for core app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Frontend routes
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.projects_page, name='projects'),
    path('projects/<uuid:project_id>/', views.project_detail, name='project_detail'),
    
    # API routes will be added later
]