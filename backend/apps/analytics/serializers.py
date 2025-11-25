"""
Serializers for Analytics app
"""
from rest_framework import serializers
from .models import DashboardMetric


class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = ['id', 'company', 'metric_type', 'metric_value', 'metric_data',
                 'period_start', 'period_end', 'created_at']
        read_only_fields = ['created_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_inspections = serializers.IntegerField()
    completed_inspections = serializers.IntegerField()
    pending_inspections = serializers.IntegerField()
    total_issues = serializers.IntegerField()
    open_issues = serializers.IntegerField()
    resolved_issues = serializers.IntegerField()
    total_reports = serializers.IntegerField()
    recent_inspections = serializers.ListField()
