"""
URL configuration for Reports app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReportTemplateViewSet, ReportViewSet, ReportSectionViewSet,
    ReportShareViewSet, ReportAnnotationViewSet, ReportScheduleViewSet
)

router = DefaultRouter()

router.register(r'templates', ReportTemplateViewSet, basename='report-template')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'sections', ReportSectionViewSet, basename='report-section')
router.register(r'shares', ReportShareViewSet, basename='report-share')
router.register(r'annotations', ReportAnnotationViewSet, basename='report-annotation')
router.register(r'schedules', ReportScheduleViewSet, basename='report-schedule')

urlpatterns = [
    path('', include(router.urls)),
]
