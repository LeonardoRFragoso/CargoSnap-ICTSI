"""
Views for Analytics app
Dashboard and statistics endpoints
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import DashboardMetric
from .serializers import DashboardMetricSerializer, DashboardStatsSerializer


class AnalyticsViewSet(viewsets.ViewSet):
    """Analytics and Dashboard endpoints"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get dashboard statistics"""
        from apps.inspections.models import Inspection
        from apps.issues.models import Issue
        from apps.reports.models import Report
        
        company = request.user.company
        
        # Date range (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Inspections stats
        inspections = Inspection.objects.filter(company=company)
        total_inspections = inspections.count()
        completed_inspections = inspections.filter(status='COMPLETED').count()
        pending_inspections = inspections.filter(status__in=['DRAFT', 'IN_PROGRESS']).count()
        
        # Issues stats
        issues = Issue.objects.filter(company=company)
        total_issues = issues.count()
        open_issues = issues.filter(status='OPEN').count()
        resolved_issues = issues.filter(status='RESOLVED').count()
        
        # Reports stats
        reports = Report.objects.filter(inspection__company=company)
        total_reports = reports.count()
        
        # Recent inspections
        recent = inspections.order_by('-created_at')[:5].values(
            'id', 'reference_number', 'title', 'status', 'created_at'
        )
        
        data = {
            'total_inspections': total_inspections,
            'completed_inspections': completed_inspections,
            'pending_inspections': pending_inspections,
            'total_issues': total_issues,
            'open_issues': open_issues,
            'resolved_issues': resolved_issues,
            'total_reports': total_reports,
            'recent_inspections': list(recent)
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inspections_by_status(self, request):
        """Get inspections grouped by status"""
        from apps.inspections.models import Inspection
        
        company = request.user.company
        data = Inspection.objects.filter(company=company).values('status').annotate(
            count=Count('id')
        )
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def issues_by_priority(self, request):
        """Get issues grouped by priority"""
        from apps.issues.models import Issue
        
        company = request.user.company
        data = Issue.objects.filter(company=company).values('priority').annotate(
            count=Count('id')
        )
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def inspections_timeline(self, request):
        """Get inspections over time"""
        from apps.inspections.models import Inspection
        from django.db.models.functions import TruncDate
        
        company = request.user.company
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)
        
        data = Inspection.objects.filter(
            company=company,
            created_at__gte=start_date
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        return Response(data)


class DashboardMetricViewSet(viewsets.ModelViewSet):
    """CRUD for Dashboard Metrics"""
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
