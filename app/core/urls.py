"""
URL configuration for core app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics_page, name='analytics'),
    path('data/', views.data_page, name='data'),
    path('reports/', views.reports_page, name='reports'),
]