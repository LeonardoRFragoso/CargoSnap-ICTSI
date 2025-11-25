"""
Views for Issues app
Complete ViewSets for issue management
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsAuthenticated, IsSameCompany, IsAdminOrManager
from .models import (
    IssueCategory, Issue, IssuePhoto, IssueComment,
    IssueTask, IssueTemplate
)
from .serializers import (
    IssueCategorySerializer, IssueListSerializer, IssueDetailSerializer,
    IssuePhotoSerializer, IssueCommentSerializer, IssueTaskSerializer,
    IssueTemplateSerializer
)


class IssueCategoryViewSet(viewsets.ModelViewSet):
    """CRUD for Issue Categories"""
    queryset = IssueCategory.objects.all()
    serializer_class = IssueCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class IssueViewSet(viewsets.ModelViewSet):
    """CRUD for Issues"""
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated, IsSameCompany]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'severity', 'category', 'assigned_to']
    search_fields = ['reference_number', 'title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return IssueListSerializer
        return IssueDetailSerializer
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an issue"""
        from django.utils import timezone
        issue = self.get_object()
        issue.status = 'RESOLVED'
        issue.resolved_at = timezone.now()
        issue.resolved_by = request.user
        issue.resolution_notes = request.data.get('notes', '')
        issue.save()
        return Response({'status': 'Issue resolved'})
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close an issue"""
        from django.utils import timezone
        issue = self.get_object()
        issue.status = 'CLOSED'
        issue.closed_at = timezone.now()
        issue.save()
        return Response({'status': 'Issue closed'})


class IssuePhotoViewSet(viewsets.ModelViewSet):
    """CRUD for Issue Photos"""
    queryset = IssuePhoto.objects.all()
    serializer_class = IssuePhotoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issue', 'photo_type']
    
    def get_queryset(self):
        return self.queryset.filter(issue__company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(taken_by=self.request.user)


class IssueCommentViewSet(viewsets.ModelViewSet):
    """CRUD for Issue Comments"""
    queryset = IssueComment.objects.all()
    serializer_class = IssueCommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issue', 'is_internal']
    
    def get_queryset(self):
        queryset = self.queryset.filter(issue__company=self.request.user.company)
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(is_internal=False)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IssueTaskViewSet(viewsets.ModelViewSet):
    """CRUD for Issue Tasks"""
    queryset = IssueTask.objects.all()
    serializer_class = IssueTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issue', 'status', 'assigned_to']
    
    def get_queryset(self):
        return self.queryset.filter(issue__company=self.request.user.company)


class IssueTemplateViewSet(viewsets.ModelViewSet):
    """CRUD for Issue Templates"""
    queryset = IssueTemplate.objects.all()
    serializer_class = IssueTemplateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
