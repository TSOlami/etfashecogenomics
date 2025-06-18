"""
URL configuration for accounts app.
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # API URLs
    path('api/register/', views.register_user, name='api_register'),
    path('api/login/', views.login_user, name='api_login'),
    path('api/logout/', views.logout_user, name='api_logout'),
    
    # Frontend URLs
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
]