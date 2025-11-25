"""
Serializers for Issues app
"""
from rest_framework import serializers
from .models import (
    IssueCategory, Issue, IssuePhoto, IssueComment,
    IssueAttachment, IssueTask, IssueHistory, IssueTemplate
)


class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = [
            'id', 'company', 'name', 'description', 'color', 'icon',
            'default_priority', 'default_sla_hours', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']


class IssuePhotoSerializer(serializers.ModelSerializer):
    taken_by_name = serializers.CharField(source='taken_by.full_name', read_only=True)
    
    class Meta:
        model = IssuePhoto
        fields = [
            'id', 'issue', 'photo', 'thumbnail', 'caption', 'photo_type',
            'taken_at', 'taken_by', 'taken_by_name', 'sequence_number'
        ]
        read_only_fields = ['taken_at', 'taken_by']


class IssueAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueAttachment
        fields = [
            'id', 'comment', 'file', 'file_name', 'file_size_mb',
            'file_type', 'created_at'
        ]
        read_only_fields = ['created_at']


class IssueCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    attachments = IssueAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = IssueComment
        fields = [
            'id', 'issue', 'user', 'user_name', 'comment', 'is_internal',
            'has_attachments', 'attachments', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']


class IssueTaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    completed_by_name = serializers.CharField(source='completed_by.full_name', read_only=True)
    
    class Meta:
        model = IssueTask
        fields = [
            'id', 'issue', 'title', 'description', 'status',
            'assigned_to', 'assigned_to_name', 'due_date',
            'completed_at', 'completed_by', 'completed_by_name',
            'sequence', 'created_at'
        ]
        read_only_fields = ['completed_by', 'completed_at', 'created_at']


class IssueHistorySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = IssueHistory
        fields = [
            'id', 'issue', 'user', 'user_name', 'action', 'field_name',
            'old_value', 'new_value', 'changed_at', 'ip_address'
        ]
        read_only_fields = ['changed_at']


class IssueListSerializer(serializers.ModelSerializer):
    """Lightweight for list views"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    inspection_reference = serializers.CharField(source='inspection.reference_number', read_only=True)
    reported_by_name = serializers.CharField(source='reported_by.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    
    class Meta:
        model = Issue
        fields = [
            'id', 'company', 'company_name', 'inspection', 'inspection_reference',
            'category', 'category_name', 'reference_number', 'title',
            'priority', 'severity', 'status',
            'reported_by', 'reported_by_name', 'assigned_to', 'assigned_to_name',
            'detected_at', 'due_date', 'resolved_at', 'created_at'
        ]
        read_only_fields = ['reference_number', 'detected_at', 'created_at']


class IssueDetailSerializer(serializers.ModelSerializer):
    """Complete for detail views"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    inspection_reference = serializers.CharField(source='inspection.reference_number', read_only=True)
    reported_by_name = serializers.CharField(source='reported_by.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.full_name', read_only=True)
    
    photos = IssuePhotoSerializer(many=True, read_only=True)
    comments = IssueCommentSerializer(many=True, read_only=True)
    tasks = IssueTaskSerializer(many=True, read_only=True)
    history = IssueHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Issue
        fields = [
            'id', 'company', 'company_name', 'inspection', 'inspection_reference',
            'category', 'category_name', 'reference_number', 'title', 'description',
            'priority', 'severity', 'status',
            'reported_by', 'reported_by_name', 'assigned_to', 'assigned_to_name',
            'assigned_team', 'location', 'latitude', 'longitude',
            'detected_at', 'due_date', 'resolved_at', 'closed_at',
            'resolved_by', 'resolved_by_name', 'resolution_notes',
            'root_cause', 'preventive_action',
            'estimated_cost', 'actual_cost', 'custom_fields',
            'photos', 'comments', 'tasks', 'history',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['reference_number', 'detected_at', 'created_at', 'updated_at']


class IssueTemplateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = IssueTemplate
        fields = [
            'id', 'company', 'category', 'category_name', 'name',
            'description_template', 'default_priority', 'default_severity',
            'default_assigned_team', 'checklist_items',
            'usage_count', 'is_active', 'created_at'
        ]
        read_only_fields = ['usage_count', 'created_at']
