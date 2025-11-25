"""
URL configuration for Analytics app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet, DashboardMetricViewSet

router = DefaultRouter()

router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'metrics', DashboardMetricViewSet, basename='dashboard-metric')

urlpatterns = [
    path('', include(router.urls)),
]
