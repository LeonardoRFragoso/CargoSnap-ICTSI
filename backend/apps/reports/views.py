"""
Views for Reports app
Complete ViewSets for report generation and management
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsAuthenticated, IsSameCompany, IsAdminOrManager, CanGenerateReports
from .models import (
    ReportTemplate, Report, ReportSection, ReportShare,
    ReportAnnotation, ReportSchedule
)
from .serializers import (
    ReportTemplateListSerializer, ReportTemplateDetailSerializer,
    ReportListSerializer, ReportDetailSerializer, ReportSectionSerializer,
    ReportShareSerializer, ReportAnnotationSerializer, ReportScheduleSerializer
)


class ReportTemplateViewSet(viewsets.ModelViewSet):
    """CRUD for Report Templates"""
    queryset = ReportTemplate.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['inspection_type', 'format', 'is_active', 'is_default']
    search_fields = ['name', 'code']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReportTemplateListSerializer
        return ReportTemplateDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )


class ReportViewSet(viewsets.ModelViewSet):
    """CRUD for Generated Reports"""
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated, CanGenerateReports]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inspection', 'template', 'status', 'is_public']
    search_fields = ['inspection__reference_number']
    ordering_fields = ['generated_at', 'file_size_mb']
    ordering = ['-generated_at']
    
    def get_queryset(self):
        return self.queryset.filter(inspection__company=self.request.user.company)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReportListSerializer
        return ReportDetailSerializer
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a new report"""
        inspection_id = request.data.get('inspection_id')
        template_id = request.data.get('template_id')
        
        if not inspection_id or not template_id:
            return Response(
                {'error': 'inspection_id and template_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create report record
        from apps.inspections.models import Inspection
        from django.utils import timezone
        import time
        
        start_time = time.time()
        
        report = Report.objects.create(
            inspection_id=inspection_id,
            template_id=template_id,
            status='GENERATING',
            generated_by=request.user
        )
        
        # TODO: Implement actual PDF generation with ReportLab/WeasyPrint
        # For now, just mark as completed
        report.status = 'COMPLETED'
        report.generation_time_seconds = round(time.time() - start_time, 2)
        report.save()
        
        serializer = ReportDetailSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share a report"""
        report = self.get_object()
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        share = ReportShare.objects.create(
            report=report,
            shared_with_email=email,
            shared_with_name=request.data.get('name', ''),
            can_download=request.data.get('can_download', True),
            can_print=request.data.get('can_print', True),
            shared_by=request.user,
            message=request.data.get('message', '')
        )
        
        serializer = ReportShareSerializer(share)
        return Response(serializer.data)


class ReportSectionViewSet(viewsets.ModelViewSet):
    """CRUD for Report Sections"""
    queryset = ReportSection.objects.all()
    serializer_class = ReportSectionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['template', 'is_enabled']
    
    def get_queryset(self):
        return self.queryset.filter(template__company=self.request.user.company)


class ReportShareViewSet(viewsets.ModelViewSet):
    """CRUD for Report Shares"""
    queryset = ReportShare.objects.all()
    serializer_class = ReportShareSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report']
    
    def get_queryset(self):
        return self.queryset.filter(report__inspection__company=self.request.user.company)


class ReportAnnotationViewSet(viewsets.ModelViewSet):
    """CRUD for Report Annotations"""
    queryset = ReportAnnotation.objects.all()
    serializer_class = ReportAnnotationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report', 'is_resolved']
    
    def get_queryset(self):
        return self.queryset.filter(report__inspection__company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an annotation"""
        from django.utils import timezone
        annotation = self.get_object()
        annotation.is_resolved = True
        annotation.resolved_by = request.user
        annotation.resolved_at = timezone.now()
        annotation.save()
        return Response({'status': 'Annotation resolved'})


class ReportScheduleViewSet(viewsets.ModelViewSet):
    """CRUD for Report Schedules"""
    queryset = ReportSchedule.objects.all()
    serializer_class = ReportScheduleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['frequency', 'is_active']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def run_now(self, request, pk=None):
        """Execute schedule immediately"""
        from django.utils import timezone
        schedule = self.get_object()
        # TODO: Implement actual report generation
        schedule.last_run_at = timezone.now()
        schedule.run_count += 1
        schedule.save()
        return Response({'status': 'Schedule executed'})
