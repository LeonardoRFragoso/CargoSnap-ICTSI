"""
URL configuration for CargoSnap ICTSI project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.core.views import (
    login_view, register_view, logout_view,
    password_reset_view, password_reset_done_view,
    dashboard_view
)

urlpatterns = [
    # Web Routes (HTML Templates)
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('password-reset/done/', password_reset_done_view, name='password_reset_done'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Routes
    path('api/auth/', include('apps.core.urls')),
    path('api/inspections/', include('apps.inspections.urls')),
    path('api/workflows/', include('apps.workflows.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/issues/', include('apps.issues.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = 'CargoSnap ICTSI Admin'
admin.site.site_title = 'CargoSnap ICTSI'
admin.site.index_title = 'Administração do Sistema'
