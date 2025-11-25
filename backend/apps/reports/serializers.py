"""
Serializers for Reports app
"""
from rest_framework import serializers
from .models import (
    ReportTemplate, Report, ReportSection, ReportShare,
    ReportAnnotation, ReportSchedule
)


class ReportSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSection
        fields = [
            'id', 'template', 'name', 'title', 'description', 'sequence',
            'content_type', 'content_config', 'is_enabled',
            'page_break_before', 'page_break_after', 'created_at'
        ]
        read_only_fields = ['created_at']


class ReportTemplateListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    inspection_type_name = serializers.CharField(source='inspection_type.name', read_only=True)
    section_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportTemplate
        fields = [
            'id', 'company', 'company_name', 'name', 'description', 'code',
            'inspection_type', 'inspection_type_name', 'format', 'is_active',
            'is_default', 'version', 'section_count', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_section_count(self, obj):
        return obj.sections.count()


class ReportTemplateDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    sections = ReportSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = ReportTemplate
        fields = [
            'id', 'company', 'company_name', 'name', 'description', 'code',
            'inspection_type', 'format', 'is_active', 'is_default',
            'template_file', 'html_template',
            'include_cover_page', 'include_summary', 'include_photos',
            'include_signatures', 'include_comments', 'include_metadata',
            'logo', 'header_text', 'footer_text', 'watermark_text',
            'styling', 'created_by', 'created_by_name', 'version',
            'sections', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class ReportShareSerializer(serializers.ModelSerializer):
    shared_by_name = serializers.CharField(source='shared_by.full_name', read_only=True)
    
    class Meta:
        model = ReportShare
        fields = [
            'id', 'report', 'shared_with_email', 'shared_with_name',
            'can_download', 'can_print', 'expires_at',
            'access_count', 'last_accessed_at',
            'shared_by', 'shared_by_name', 'shared_at', 'message'
        ]
        read_only_fields = ['shared_by', 'shared_at', 'access_count', 'last_accessed_at']


class ReportAnnotationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.full_name', read_only=True)
    
    class Meta:
        model = ReportAnnotation
        fields = [
            'id', 'report', 'user', 'user_name', 'text', 'page_number', 'section',
            'x_position', 'y_position', 'is_resolved', 'resolved_by',
            'resolved_by_name', 'resolved_at', 'created_at'
        ]
        read_only_fields = ['user', 'resolved_by', 'resolved_at', 'created_at']


class ReportListSerializer(serializers.ModelSerializer):
    inspection_reference = serializers.CharField(source='inspection.reference_number', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.full_name', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'inspection', 'inspection_reference', 'template', 'template_name',
            'file', 'file_size_mb', 'status', 'generated_by', 'generated_by_name',
            'generated_at', 'generation_time_seconds', 'is_public', 'version'
        ]
        read_only_fields = ['generated_by', 'generated_at']


class ReportDetailSerializer(serializers.ModelSerializer):
    inspection_reference = serializers.CharField(source='inspection.reference_number', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.full_name', read_only=True)
    shares = ReportShareSerializer(many=True, read_only=True)
    annotations = ReportAnnotationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'inspection', 'inspection_reference', 'template', 'template_name',
            'file', 'file_size_mb', 'status', 'error_message',
            'generated_by', 'generated_by_name', 'generated_at', 'generation_time_seconds',
            'is_public', 'public_url', 'access_code', 'version', 'parent_report',
            'shares', 'annotations', 'created_at'
        ]
        read_only_fields = ['generated_by', 'generated_at', 'created_at']


class ReportScheduleSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = ReportSchedule
        fields = [
            'id', 'company', 'template', 'template_name', 'name', 'description',
            'frequency', 'is_active', 'inspection_type', 'status_filter',
            'date_range_days', 'recipients', 'last_run_at', 'next_run_at',
            'run_count', 'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['created_by', 'last_run_at', 'run_count', 'created_at']
