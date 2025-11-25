"""
Models for Workflows app
Custom workflow builder with steps, forms, and conditional logic
"""
from django.db import models
from apps.core.models import User, Company, BaseModel
from apps.inspections.models import InspectionType


class Workflow(BaseModel):
    """Main workflow template"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='workflows')
    
    # Basic information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True)
    
    # Configuration
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.SET_NULL, null=True, blank=True, related_name='workflows')
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)  # Default workflow for inspection type
    
    # Settings
    requires_approval = models.BooleanField(default=False)
    allow_skip_steps = models.BooleanField(default=False)
    auto_generate_report = models.BooleanField(default=True)
    
    # Metadata
    version = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_workflows')
    
    class Meta:
        ordering = ['name']
        unique_together = ['company', 'code']
    
    def __str__(self):
        return f"{self.name} (v{self.version})"


class WorkflowStep(BaseModel):
    """Individual steps in a workflow"""
    STEP_TYPES = [
        ('FORM', 'Fill Form'),
        ('PHOTO', 'Take Photo'),
        ('VIDEO', 'Record Video'),
        ('SCAN', 'Scan Reference'),
        ('SIGNATURE', 'Collect Signature'),
        ('APPROVAL', 'Approval Required'),
        ('NOTIFICATION', 'Send Notification'),
        ('CUSTOM', 'Custom Action'),
    ]
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='steps')
    
    # Step configuration
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    step_type = models.CharField(max_length=20, choices=STEP_TYPES)
    sequence = models.IntegerField(default=0)
    
    # Behavior
    is_required = models.BooleanField(default=True)
    is_skippable = models.BooleanField(default=False)
    min_photos = models.IntegerField(default=0)  # For PHOTO type
    max_photos = models.IntegerField(null=True, blank=True)
    
    # Conditional logic
    condition_field = models.CharField(max_length=100, blank=True)  # Field to check
    condition_operator = models.CharField(max_length=20, blank=True)  # equals, contains, etc.
    condition_value = models.CharField(max_length=200, blank=True)  # Value to compare
    
    # Configuration (JSON for flexibility)
    config = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['sequence']
        unique_together = ['workflow', 'sequence']
    
    def __str__(self):
        return f"{self.workflow.name} - Step {self.sequence}: {self.name}"


class WorkflowForm(BaseModel):
    """Custom forms for workflow steps"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='workflow_forms')
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    # Configuration
    config = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class WorkflowFormField(BaseModel):
    """Fields in a custom form"""
    FIELD_TYPES = [
        ('TEXT', 'Text Input'),
        ('NUMBER', 'Number'),
        ('DATE', 'Date'),
        ('TIME', 'Time'),
        ('DATETIME', 'Date & Time'),
        ('TEXTAREA', 'Text Area'),
        ('SELECT', 'Dropdown'),
        ('MULTISELECT', 'Multiple Select'),
        ('CHECKBOX', 'Checkbox'),
        ('RADIO', 'Radio Buttons'),
        ('EMAIL', 'Email'),
        ('PHONE', 'Phone Number'),
        ('URL', 'URL'),
        ('FILE', 'File Upload'),
    ]
    
    form = models.ForeignKey(WorkflowForm, on_delete=models.CASCADE, related_name='fields')
    
    # Field configuration
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    placeholder = models.CharField(max_length=200, blank=True)
    help_text = models.TextField(blank=True)
    
    # Validation
    is_required = models.BooleanField(default=False)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_length = models.IntegerField(null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    pattern = models.CharField(max_length=200, blank=True)  # Regex pattern
    
    # Options for SELECT, MULTISELECT, RADIO
    options = models.JSONField(default=list, blank=True)
    
    # Default value
    default_value = models.CharField(max_length=200, blank=True)
    
    # Display
    sequence = models.IntegerField(default=0)
    width = models.CharField(max_length=20, default='full')  # full, half, third, quarter
    
    # Conditional display
    show_if_field = models.CharField(max_length=100, blank=True)
    show_if_value = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['sequence']
    
    def __str__(self):
        return f"{self.form.name} - {self.label}"


class WorkflowStepForm(models.Model):
    """Link between workflow steps and forms"""
    step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name='form_links')
    form = models.ForeignKey(WorkflowForm, on_delete=models.CASCADE, related_name='step_links')
    is_required = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['step', 'form']
    
    def __str__(self):
        return f"{self.step.name} - {self.form.name}"


class WorkflowExecution(BaseModel):
    """Track workflow execution for an inspection"""
    from apps.inspections.models import Inspection
    
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT, related_name='executions')
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE, related_name='workflow_execution')
    
    # Status
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    
    # Progress
    current_step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_executions')
    current_step_number = models.IntegerField(default=0)
    total_steps = models.IntegerField(default=0)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Data collected
    execution_data = models.JSONField(default=dict, blank=True)  # All form responses
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.inspection.reference_number}"


class WorkflowStepExecution(BaseModel):
    """Track execution of individual workflow steps"""
    execution = models.ForeignKey(WorkflowExecution, on_delete=models.CASCADE, related_name='step_executions')
    step = models.ForeignKey(WorkflowStep, on_delete=models.PROTECT, related_name='executions')
    
    # Status
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('SKIPPED', 'Skipped'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Execution
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Data
    step_data = models.JSONField(default=dict, blank=True)  # Form responses for this step
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['step__sequence']
        unique_together = ['execution', 'step']
    
    def __str__(self):
        return f"{self.execution.inspection.reference_number} - {self.step.name}"


class WorkflowFormResponse(BaseModel):
    """Store responses to workflow forms"""
    execution = models.ForeignKey(WorkflowExecution, on_delete=models.CASCADE, related_name='form_responses')
    step_execution = models.ForeignKey(WorkflowStepExecution, on_delete=models.CASCADE, related_name='form_responses')
    form = models.ForeignKey(WorkflowForm, on_delete=models.PROTECT, related_name='responses')
    field = models.ForeignKey(WorkflowFormField, on_delete=models.PROTECT, related_name='responses')
    
    # Response value
    value = models.TextField()
    file_url = models.URLField(blank=True)  # For file uploads
    
    # Metadata
    answered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['field__sequence']
    
    def __str__(self):
        return f"{self.form.name} - {self.field.label}: {self.value[:50]}"
