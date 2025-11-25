"""
URL configuration for Core app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    CompanyViewSet,
    UserViewSet,
    AuditLogViewSet,
    NotificationViewSet,
    WebhookViewSet,
    WebhookLogViewSet,
    ApiKeyViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'users', UserViewSet, basename='user')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'webhooks', WebhookViewSet, basename='webhook')
router.register(r'webhook-logs', WebhookLogViewSet, basename='webhook-log')
router.register(r'api-keys', ApiKeyViewSet, basename='api-key')

urlpatterns = [
    # JWT Authentication
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Router URLs
    path('', include(router.urls)),
]
