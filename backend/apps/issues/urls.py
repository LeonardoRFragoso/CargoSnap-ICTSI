"""
URL configuration for Issues app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IssueCategoryViewSet, IssueViewSet, IssuePhotoViewSet,
    IssueCommentViewSet, IssueTaskViewSet, IssueTemplateViewSet
)

router = DefaultRouter()

router.register(r'categories', IssueCategoryViewSet, basename='issue-category')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'photos', IssuePhotoViewSet, basename='issue-photo')
router.register(r'comments', IssueCommentViewSet, basename='issue-comment')
router.register(r'tasks', IssueTaskViewSet, basename='issue-task')
router.register(r'templates', IssueTemplateViewSet, basename='issue-template')

urlpatterns = [
    path('', include(router.urls)),
]
