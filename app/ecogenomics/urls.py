"""
URL configuration for EcoGenomics Suite project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes - Must come before frontend routes
    path('api/auth/', include('accounts.urls')),
    
    # Frontend routes
    path('accounts/', include('accounts.urls')),  # Frontend auth routes
    path('', home_redirect, name='home'),  # Root redirect
    path('dashboard/', include('core.urls')),  # Dashboard routes
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
handler403 = 'django.views.defaults.permission_denied'