"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, LoginAttempt


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin.
    """
    list_display = [
        'email', 'username', 'full_name', 'role', 'organization',
        'is_verified', 'is_active', 'date_joined', 'storage_usage_display'
    ]
    list_filter = ['role', 'is_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'organization']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'organization', 'bio', 'avatar', 'is_verified')
        }),
        ('Storage', {
            'fields': ('storage_used', 'max_storage')
        }),
        ('Login Info', {
            'fields': ('last_login_ip',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'role', 'organization')
        }),
    )
    
    def storage_usage_display(self, obj):
        percentage = obj.storage_usage_percentage
        color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, percentage
        )
    storage_usage_display.short_description = 'Storage Usage'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile admin.
    """
    list_display = [
        'user', 'country', 'expertise_level', 'email_notifications',
        'created_at', 'updated_at'
    ]
    list_filter = ['expertise_level', 'email_notifications', 'country']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """
    Login Attempt admin.
    """
    list_display = ['email', 'ip_address', 'success', 'timestamp']
    list_filter = ['success', 'timestamp']
    search_fields = ['email', 'ip_address']
    readonly_fields = ['email', 'ip_address', 'user_agent', 'success', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False