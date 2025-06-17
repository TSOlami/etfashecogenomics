"""
URL configuration for accounts app.
"""
from django.urls import path
from . import views

app_name = 'accounts'

# API URLs - These should be accessed via /api/auth/
api_urlpatterns = [
    path('register/', views.register_user, name='api_register'),
    path('login/', views.login_user, name='api_login'),
    path('logout/', views.logout_user, name='api_logout'),
    path('profile/', views.user_profile, name='api_profile'),
    path('profile/update/', views.update_profile, name='api_update_profile'),
    path('password/change/', views.change_password, name='api_change_password'),
]

# Frontend URLs - These render HTML templates
frontend_urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]

# Export only API patterns for inclusion in main URLs
urlpatterns = api_urlpatterns