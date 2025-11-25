"""
URL configuration for Workflows app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WorkflowViewSet, WorkflowStepViewSet, WorkflowFormViewSet,
    WorkflowFormFieldViewSet, WorkflowExecutionViewSet, WorkflowStepExecutionViewSet
)

router = DefaultRouter()

router.register(r'workflows', WorkflowViewSet, basename='workflow')
router.register(r'steps', WorkflowStepViewSet, basename='workflow-step')
router.register(r'forms', WorkflowFormViewSet, basename='workflow-form')
router.register(r'form-fields', WorkflowFormFieldViewSet, basename='workflow-form-field')
router.register(r'executions', WorkflowExecutionViewSet, basename='workflow-execution')
router.register(r'step-executions', WorkflowStepExecutionViewSet, basename='workflow-step-execution')

urlpatterns = [
    path('', include(router.urls)),
]
