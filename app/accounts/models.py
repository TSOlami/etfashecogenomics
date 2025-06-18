"""
User models for the EcoGenomics Suite.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    ROLE_CHOICES = [
        ('researcher', 'Researcher'),
        ('analyst', 'Data Analyst'),
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='researcher')
    organization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Usage tracking
    storage_used = models.BigIntegerField(default=0, help_text="Storage used in bytes")
    max_storage = models.BigIntegerField(default=1073741824, help_text="Max storage in bytes (1GB default)")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def storage_usage_percentage(self):
        if self.max_storage == 0:
            return 0
        return (self.storage_used / self.max_storage) * 100
    
    def can_upload_file(self, file_size):
        """Check if user can upload a file of given size."""
        return (self.storage_used + file_size) <= self.max_storage


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    analysis_notifications = models.BooleanField(default=True)
    newsletter_subscription = models.BooleanField(default=False)
    
    # Research interests
    research_areas = models.JSONField(default=list, blank=True)
    expertise_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_userprofile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.full_name}'s Profile"