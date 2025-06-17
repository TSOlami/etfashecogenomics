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
    path('analytics/', views.analytics_page, name='analytics'),
    path('data/', views.data_page, name='data'),
    path('reports/', views.reports_page, name='reports'),
    path('samples/', views.sample_tracking_page, name='sample_tracking'),
    path('quality/', views.quality_control_page, name='quality_control'),
]