"""
Views for Workflows app
Complete ViewSets for workflow management
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsAuthenticated, IsSameCompany, IsAdminOrManager
from .models import (
    Workflow, WorkflowStep, WorkflowForm, WorkflowFormField,
    WorkflowExecution, WorkflowStepExecution
)
from .serializers import (
    WorkflowListSerializer, WorkflowDetailSerializer, WorkflowStepSerializer,
    WorkflowFormSerializer, WorkflowFormFieldSerializer, WorkflowExecutionSerializer,
    WorkflowStepExecutionSerializer
)


class WorkflowViewSet(viewsets.ModelViewSet):
    """CRUD for Workflows"""
    queryset = Workflow.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['inspection_type', 'is_active', 'is_default']
    search_fields = ['name', 'code']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return WorkflowListSerializer
        return WorkflowDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a workflow"""
        workflow = self.get_object()
        new_workflow = Workflow.objects.create(
            company=workflow.company,
            name=f"{workflow.name} (Copy)",
            description=workflow.description,
            code=f"{workflow.code}_copy",
            inspection_type=workflow.inspection_type,
            requires_approval=workflow.requires_approval,
            allow_skip_steps=workflow.allow_skip_steps,
            auto_generate_report=workflow.auto_generate_report,
            version=1,
            created_by=request.user
        )
        # Copy steps
        for step in workflow.steps.all():
            WorkflowStep.objects.create(
                workflow=new_workflow,
                name=step.name,
                description=step.description,
                step_type=step.step_type,
                sequence=step.sequence,
                is_required=step.is_required,
                is_skippable=step.is_skippable,
                config=step.config
            )
        return Response({'id': new_workflow.id, 'name': new_workflow.name})


class WorkflowStepViewSet(viewsets.ModelViewSet):
    """CRUD for Workflow Steps"""
    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workflow', 'step_type']
    
    def get_queryset(self):
        return self.queryset.filter(workflow__company=self.request.user.company)


class WorkflowFormViewSet(viewsets.ModelViewSet):
    """CRUD for Workflow Forms"""
    queryset = WorkflowForm.objects.all()
    serializer_class = WorkflowFormSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )


class WorkflowFormFieldViewSet(viewsets.ModelViewSet):
    """CRUD for Form Fields"""
    queryset = WorkflowFormField.objects.all()
    serializer_class = WorkflowFormFieldSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['form', 'field_type']
    
    def get_queryset(self):
        return self.queryset.filter(form__company=self.request.user.company)


class WorkflowExecutionViewSet(viewsets.ModelViewSet):
    """CRUD for Workflow Executions"""
    queryset = WorkflowExecution.objects.all()
    serializer_class = WorkflowExecutionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workflow', 'inspection', 'status']
    
    def get_queryset(self):
        return self.queryset.filter(workflow__company=self.request.user.company)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start workflow execution"""
        from django.utils import timezone
        execution = self.get_object()
        execution.status = 'IN_PROGRESS'
        execution.started_at = timezone.now()
        execution.save()
        return Response({'status': 'Workflow started'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete workflow execution"""
        from django.utils import timezone
        execution = self.get_object()
        execution.status = 'COMPLETED'
        execution.completed_at = timezone.now()
        execution.save()
        return Response({'status': 'Workflow completed'})


class WorkflowStepExecutionViewSet(viewsets.ModelViewSet):
    """CRUD for Step Executions"""
    queryset = WorkflowStepExecution.objects.all()
    serializer_class = WorkflowStepExecutionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['execution', 'step', 'status']
    
    def get_queryset(self):
        return self.queryset.filter(execution__workflow__company=self.request.user.company)
    
    def perform_create(self, serializer):
        from django.utils import timezone
        serializer.save(
            started_at=timezone.now(),
            completed_by=self.request.user
        )
