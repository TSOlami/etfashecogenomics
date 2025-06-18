"""
Views for the accounts app.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
import json
import logging

from .models import User, UserProfile

# Set up logging
logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """Register a new user - Demo accepts any valid data."""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        
        # Demo validation - just check required fields
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({field: [f'{field} is required.']}, status=400)
        
        # Check password match
        if data['password'] != data['password_confirm']:
            return JsonResponse({'password_confirm': ["Passwords don't match."]}, status=400)
        
        # Check if user exists
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'email': ['User with this email already exists.']}, status=400)
        
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'username': ['User with this username already exists.']}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
            role=data.get('role', 'researcher'),
            organization=data.get('organization', '')
        )
        
        # Create profile
        UserProfile.objects.create(user=user)
        
        # Create token
        token, created = Token.objects.get_or_create(user=user)
        
        return JsonResponse({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'organization': user.organization,
            },
            'token': token.key
        }, status=201)
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return JsonResponse({'error': 'Registration failed'}, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """Login user - Demo accepts any username/password combination."""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'detail': 'Email and password are required.'}, status=400)
        
        # Try to authenticate
        user = authenticate(username=email, password=password)
        
        if user and user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                },
                'token': token.key
            }, status=200)
        else:
            return JsonResponse({'detail': 'Invalid credentials.'}, status=400)
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return JsonResponse({'error': 'Login failed'}, status=500)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """Logout user by deleting token."""
    try:
        request.user.auth_token.delete()
        return JsonResponse({'message': 'Logout successful'}, status=200)
    except:
        return JsonResponse({'message': 'Logout successful'}, status=200)


@ensure_csrf_cookie
def login_page(request):
    """Render login page."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'accounts/login.html')


@ensure_csrf_cookie
def register_page(request):
    """Render registration page."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'accounts/register.html')


def logout_view(request):
    """Handle logout and redirect."""
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'auth_token'):
                    request.user.auth_token.delete()
            except:
                pass
            logout(request)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Logout successful', 'redirect': '/accounts/login/'})
        
        messages.success(request, 'You have been successfully logged out.')
        return redirect('accounts:login')
    
    return redirect('accounts:login')