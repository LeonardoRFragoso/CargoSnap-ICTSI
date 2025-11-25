"""
Admin configuration for Issues app
"""
from django.contrib import admin
from .models import (
    IssueCategory, Issue, IssuePhoto, IssueComment, 
    IssueAttachment, IssueTask, IssueHistory, IssueTemplate
)


@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'default_priority', 'is_active']
    list_filter = ['company', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'title', 'company', 'priority', 'severity', 'status', 'assigned_to', 'created_at']
    list_filter = ['company', 'status', 'priority', 'severity', 'category']
    search_fields = ['reference_number', 'title', 'description']
    readonly_fields = ['reference_number', 'detected_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'inspection', 'category', 'reference_number')
        }),
        ('Issue Details', {
            'fields': ('title', 'description', 'priority', 'severity', 'status')
        }),
        ('Assignment', {
            'fields': ('reported_by', 'assigned_to', 'assigned_team')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('detected_at', 'due_date', 'resolved_at', 'closed_at')
        }),
        ('Resolution', {
            'fields': ('resolved_by', 'resolution_notes', 'root_cause', 'preventive_action'),
            'classes': ('collapse',)
        }),
        ('Financial', {
            'fields': ('estimated_cost', 'actual_cost'),
            'classes': ('collapse',)
        }),
    )


@admin.register(IssuePhoto)
class IssuePhotoAdmin(admin.ModelAdmin):
    list_display = ['issue', 'photo_type', 'sequence_number', 'taken_by', 'taken_at']
    list_filter = ['photo_type']


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ['issue', 'user', 'is_internal', 'has_attachments', 'created_at']
    list_filter = ['is_internal', 'created_at']


@admin.register(IssueTask)
class IssueTaskAdmin(admin.ModelAdmin):
    list_display = ['issue', 'title', 'status', 'assigned_to', 'due_date']
    list_filter = ['status']


@admin.register(IssueTemplate)
class IssueTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'category', 'usage_count', 'is_active']
    list_filter = ['company', 'category', 'is_active']


admin.site.register(IssueAttachment)
admin.site.register(IssueHistory)
