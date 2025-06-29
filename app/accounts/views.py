"""
Views for the accounts app.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import logging

from .models import User, LoginAttempt
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileDetailSerializer,
    PasswordChangeSerializer
)

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
    """
    Register a new user.
    """
    logger.info(f"Registration request received - Method: {request.method}")
    logger.info(f"Content-Type: {request.content_type}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    # Handle different content types
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        
        logger.info(f"Parsed data: {data}")
    except Exception as e:
        logger.error(f"Error parsing request data: {str(e)}")
        return JsonResponse({
            'error': 'Invalid request data format'
        }, status=400)
    
    serializer = UserRegistrationSerializer(data=data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            # Log successful registration
            LoginAttempt.objects.create(
                email=user.email,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True
            )
            
            logger.info(f"User {user.email} registered successfully")
            
            response_data = {
                'message': 'User registered successfully',
                'user': UserProfileSerializer(user).data,
                'token': token.key
            }
            
            return JsonResponse(response_data, status=201)
            
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")
            return JsonResponse({
                'error': 'Registration failed due to server error',
                'details': str(e)
            }, status=500)
    
    logger.warning(f"Registration failed with errors: {serializer.errors}")
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """
    Login user and return token.
    """
    logger.info(f"Login request received - Method: {request.method}")
    logger.info(f"Content-Type: {request.content_type}")
    
    # Handle different content types
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.data
        
        logger.info(f"Login attempt for email: {data.get('email', 'unknown')}")
    except Exception as e:
        logger.error(f"Error parsing login data: {str(e)}")
        return JsonResponse({
            'error': 'Invalid request data format'
        }, status=400)
    
    serializer = UserLoginSerializer(data=data)
    if serializer.is_valid():
        try:
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Update last login info
            user.last_login = timezone.now()
            user.last_login_ip = get_client_ip(request)
            user.save(update_fields=['last_login', 'last_login_ip'])
            
            # Log successful login
            LoginAttempt.objects.create(
                email=user.email,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True
            )
            
            logger.info(f"User {user.email} logged in successfully")
            
            response_data = {
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'token': token.key
            }
            
            return JsonResponse(response_data, status=200)
            
        except Exception as e:
            logger.error(f"Error during user login: {str(e)}")
            return JsonResponse({
                'error': 'Login failed due to server error',
                'details': str(e)
            }, status=500)
    
    # Log failed login attempt
    email = data.get('email', '')
    if email:
        LoginAttempt.objects.create(
            email=email,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=False
        )
    
    logger.warning(f"Login failed for email: {email} with errors: {serializer.errors}")
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """
    Logout user by deleting token.
    """
    try:
        request.user.auth_token.delete()
        logger.info(f"User {request.user.email} logged out successfully")
        return JsonResponse({'message': 'Logout successful'}, status=200)
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return JsonResponse({'message': 'Logout successful'}, status=200)


def logout_view(request):
    """
    Handle logout and redirect to login page.
    """
    if request.method == 'POST':
        # Handle logout
        if request.user.is_authenticated:
            try:
                # Delete auth token if exists
                if hasattr(request.user, 'auth_token'):
                    request.user.auth_token.delete()
            except:
                pass
            
            # End Django session
            logout(request)
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Logout successful', 'redirect': '/accounts/login/'})
        
        # Redirect to login page with success message
        messages.success(request, 'You have been successfully logged out.')
        return redirect('accounts:login')
    
    # GET request - redirect to login
    return redirect('accounts:login')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Get current user profile.
    """
    serializer = UserProfileDetailSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """
    Update user profile.
    """
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """
    Change user password.
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        # Delete all tokens to force re-login
        Token.objects.filter(user=request.user).delete()
        return Response({'message': 'Password changed successfully. Please login again.'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Frontend Views
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


@login_required
def profile_page(request):
    """Render user profile page."""
    return render(request, 'accounts/profile.html')


# Redirect root to dashboard if authenticated, otherwise to login
def home_redirect(request):
    """Redirect home page based on authentication status."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    else:
        return redirect('accounts:login')