"""
Models for Reports app
Automated report generation with templates and customization
"""
from django.db import models
from django.core.validators import FileExtensionValidator
from apps.core.models import User, Company, BaseModel
from apps.inspections.models import Inspection, InspectionType


class ReportTemplate(BaseModel):
    """Templates for generating reports"""
    FORMAT_CHOICES = [
        ('PDF', 'PDF Document'),
        ('EXCEL', 'Excel Spreadsheet'),
        ('WORD', 'Word Document'),
        ('HTML', 'HTML'),
        ('JSON', 'JSON'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='report_templates')
    
    # Basic information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50, unique=True)
    
    # Configuration
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.SET_NULL, null=True, blank=True, related_name='report_templates')
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='PDF')
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Template content
    template_file = models.FileField(
        upload_to='report_templates/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['html', 'docx', 'xlsx'])]
    )
    html_template = models.TextField(blank=True)  # HTML template string
    
    # Sections to include
    include_cover_page = models.BooleanField(default=True)
    include_summary = models.BooleanField(default=True)
    include_photos = models.BooleanField(default=True)
    include_signatures = models.BooleanField(default=True)
    include_comments = models.BooleanField(default=True)
    include_metadata = models.BooleanField(default=True)
    
    # Customization
    logo = models.ImageField(upload_to='report_templates/logos/', blank=True)
    header_text = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)
    watermark_text = models.CharField(max_length=100, blank=True)
    
    # Styling (JSON)
    styling = models.JSONField(default=dict, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_templates')
    version = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['name']
        unique_together = ['company', 'code']
    
    def __str__(self):
        return f"{self.name} ({self.format})"


class Report(BaseModel):
    """Generated reports"""
    STATUS_CHOICES = [
        ('GENERATING', 'Generating'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('ARCHIVED', 'Archived'),
    ]
    
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='reports')
    template = models.ForeignKey(ReportTemplate, on_delete=models.PROTECT, related_name='generated_reports')
    
    # Report file
    file = models.FileField(upload_to='reports/%Y/%m/%d/', blank=True)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='GENERATING')
    error_message = models.TextField(blank=True)
    
    # Generation info
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    generation_time_seconds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Sharing
    is_public = models.BooleanField(default=False)
    public_url = models.URLField(blank=True)
    access_code = models.CharField(max_length=50, blank=True)  # For secure sharing
    
    # Versioning
    version = models.IntegerField(default=1)
    parent_report = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='versions')
    
    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['inspection', 'status']),
            models.Index(fields=['access_code']),
        ]
    
    def __str__(self):
        return f"Report for {self.inspection.reference_number} - {self.template.name}"


class ReportSection(BaseModel):
    """Custom sections in a report template"""
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='sections')
    
    # Section configuration
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sequence = models.IntegerField(default=0)
    
    # Content
    content_type = models.CharField(max_length=50)  # photos, table, text, chart, etc.
    content_config = models.JSONField(default=dict, blank=True)
    
    # Display
    is_enabled = models.BooleanField(default=True)
    page_break_before = models.BooleanField(default=False)
    page_break_after = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sequence']
    
    def __str__(self):
        return f"{self.template.name} - {self.title}"


class ReportShare(BaseModel):
    """Track report sharing and access"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='shares')
    
    # Recipient
    shared_with_email = models.EmailField()
    shared_with_name = models.CharField(max_length=200, blank=True)
    
    # Sharing settings
    can_download = models.BooleanField(default=True)
    can_print = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Access tracking
    access_count = models.IntegerField(default=0)
    last_accessed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    shared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-shared_at']
    
    def __str__(self):
        return f"Share to {self.shared_with_email} - {self.report}"


class ReportAnnotation(BaseModel):
    """Annotations/comments on generated reports"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='annotations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Annotation
    text = models.TextField()
    page_number = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=100, blank=True)
    
    # Position (for PDF annotations)
    x_position = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    y_position = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Metadata
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_annotations')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Annotation on {self.report} by {self.user}"


class ReportSchedule(BaseModel):
    """Schedule automatic report generation"""
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('ON_COMPLETION', 'On Inspection Completion'),
        ('ON_APPROVAL', 'On Inspection Approval'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='report_schedules')
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='schedules')
    
    # Schedule configuration
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    is_active = models.BooleanField(default=True)
    
    # Filters
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.SET_NULL, null=True, blank=True)
    status_filter = models.JSONField(default=list, blank=True)  # List of statuses to include
    date_range_days = models.IntegerField(default=30)  # Look back X days
    
    # Distribution
    recipients = models.JSONField(default=list, blank=True)  # List of email addresses
    
    # Execution
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    run_count = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.frequency})"
