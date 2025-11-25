"""
Serializers for Workflows app
"""
from rest_framework import serializers
from .models import (
    Workflow, WorkflowStep, WorkflowForm, WorkflowFormField,
    WorkflowStepForm, WorkflowExecution, WorkflowStepExecution,
    WorkflowFormResponse
)


class WorkflowFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowFormField
        fields = [
            'id', 'form', 'label', 'field_type', 'placeholder', 'help_text',
            'is_required', 'min_value', 'max_value', 'min_length', 'max_length',
            'pattern', 'options', 'default_value', 'sequence', 'width',
            'show_if_field', 'show_if_value', 'created_at'
        ]
        read_only_fields = ['created_at']


class WorkflowFormSerializer(serializers.ModelSerializer):
    fields = WorkflowFormFieldSerializer(many=True, read_only=True)
    field_count = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkflowForm
        fields = [
            'id', 'company', 'name', 'description', 'code', 'is_active',
            'config', 'created_by', 'fields', 'field_count', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']
    
    def get_field_count(self, obj):
        return obj.fields.count()


class WorkflowStepSerializer(serializers.ModelSerializer):
    forms = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkflowStep
        fields = [
            'id', 'workflow', 'name', 'description', 'step_type', 'sequence',
            'is_required', 'is_skippable', 'min_photos', 'max_photos',
            'condition_field', 'condition_operator', 'condition_value',
            'config', 'forms', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_forms(self, obj):
        """Return forms with their fields properly nested"""
        form_links = obj.form_links.select_related('form').prefetch_related('form__fields').all()
        return [
            {
                'id': link.form.id,
                'name': link.form.name,
                'description': link.form.description,
                'is_required': link.is_required,
                'fields': WorkflowFormFieldSerializer(link.form.fields.all(), many=True).data
            }
            for link in form_links
        ]


class WorkflowStepFormSerializer(serializers.ModelSerializer):
    form = WorkflowFormSerializer(read_only=True)
    form_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = WorkflowStepForm
        fields = ['id', 'step', 'form', 'form_id', 'is_required']


class WorkflowListSerializer(serializers.ModelSerializer):
    """Lightweight for list views"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    inspection_type_name = serializers.CharField(source='inspection_type.name', read_only=True)
    step_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Workflow
        fields = [
            'id', 'company', 'company_name', 'name', 'description', 'code',
            'inspection_type', 'inspection_type_name', 'is_active', 'is_default',
            'requires_approval', 'allow_skip_steps', 'auto_generate_report',
            'version', 'step_count', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_step_count(self, obj):
        return obj.steps.count()


class WorkflowDetailSerializer(serializers.ModelSerializer):
    """Complete for detail views"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    inspection_type_name = serializers.CharField(source='inspection_type.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    steps = WorkflowStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Workflow
        fields = [
            'id', 'company', 'company_name', 'name', 'description', 'code',
            'inspection_type', 'inspection_type_name', 'is_active', 'is_default',
            'requires_approval', 'allow_skip_steps', 'auto_generate_report',
            'version', 'created_by', 'created_by_name', 'steps',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class WorkflowFormResponseSerializer(serializers.ModelSerializer):
    field_label = serializers.CharField(source='field.label', read_only=True)
    answered_by_name = serializers.CharField(source='answered_by.full_name', read_only=True)
    
    class Meta:
        model = WorkflowFormResponse
        fields = [
            'id', 'execution', 'step_execution', 'form', 'field', 'field_label',
            'value', 'file_url', 'answered_by', 'answered_by_name', 'answered_at'
        ]
        read_only_fields = ['answered_by', 'answered_at']


class WorkflowStepExecutionSerializer(serializers.ModelSerializer):
    step_name = serializers.CharField(source='step.name', read_only=True)
    step_type = serializers.CharField(source='step.step_type', read_only=True)
    completed_by_name = serializers.CharField(source='completed_by.full_name', read_only=True)
    form_responses = WorkflowFormResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkflowStepExecution
        fields = [
            'id', 'execution', 'step', 'step_name', 'step_type', 'status',
            'started_at', 'completed_at', 'completed_by', 'completed_by_name',
            'step_data', 'notes', 'form_responses', 'created_at'
        ]
        read_only_fields = ['completed_by', 'created_at']


class WorkflowExecutionSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(source='workflow.name', read_only=True)
    inspection_reference = serializers.CharField(source='inspection.reference_number', read_only=True)
    current_step_name = serializers.CharField(source='current_step.name', read_only=True)
    step_executions = WorkflowStepExecutionSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkflowExecution
        fields = [
            'id', 'workflow', 'workflow_name', 'inspection', 'inspection_reference',
            'status', 'current_step', 'current_step_name', 'current_step_number',
            'total_steps', 'started_at', 'completed_at', 'execution_data',
            'step_executions', 'progress_percentage', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_progress_percentage(self, obj):
        if obj.total_steps == 0:
            return 0
        return round((obj.current_step_number / obj.total_steps) * 100, 2)
