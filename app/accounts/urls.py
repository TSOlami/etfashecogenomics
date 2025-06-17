"""
URL configuration for accounts app.
"""
from django.urls import path
from . import views

app_name = 'accounts'

# API URLs
api_urlpatterns = [
    path('api/register/', views.register_user, name='api_register'),
    path('api/login/', views.login_user, name='api_login'),
    path('api/logout/', views.logout_user, name='api_logout'),
    path('api/profile/', views.user_profile, name='api_profile'),
    path('api/profile/update/', views.update_profile, name='api_update_profile'),
    path('api/password/change/', views.change_password, name='api_change_password'),
    path('api/users/', views.UserListView.as_view(), name='api_user_list'),
]

# Frontend URLs
frontend_urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns = api_urlpatterns + frontend_urlpatterns