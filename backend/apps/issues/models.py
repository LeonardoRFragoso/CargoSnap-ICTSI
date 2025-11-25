"""
Models for Issues app
Issue/Problem management system with tracking and resolution
"""
from django.db import models
from apps.core.models import User, Company, BaseModel
from apps.inspections.models import Inspection


class IssueCategory(BaseModel):
    """Categories for organizing issues"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='issue_categories')
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#FF0000')
    icon = models.CharField(max_length=50, blank=True)
    
    # Priority defaults
    default_priority = models.CharField(max_length=20, default='MEDIUM')
    default_sla_hours = models.IntegerField(default=24)  # Service Level Agreement
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['company', 'name']
        verbose_name_plural = 'Issue Categories'
    
    def __str__(self):
        return self.name


class Issue(BaseModel):
    """Issues/Problems found during inspections"""
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
        ('REOPENED', 'Reopened'),
    ]
    
    SEVERITY_CHOICES = [
        ('MINOR', 'Minor'),
        ('MODERATE', 'Moderate'),
        ('MAJOR', 'Major'),
        ('CRITICAL', 'Critical'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='issues')
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='issues')
    category = models.ForeignKey(IssueCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    
    # Issue information
    title = models.CharField(max_length=200)
    description = models.TextField()
    reference_number = models.CharField(max_length=100, unique=True)
    
    # Classification
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MODERATE')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    # Assignment
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    assigned_team = models.CharField(max_length=100, blank=True)
    
    # Location
    location = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Dates
    detected_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_issues')
    resolution_notes = models.TextField(blank=True)
    root_cause = models.TextField(blank=True)
    preventive_action = models.TextField(blank=True)
    
    # Financial impact
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Additional data
    custom_fields = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['reference_number']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['priority', 'status']),
        ]
    
    def __str__(self):
        return f"{self.reference_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Auto-generate reference number if not provided
        if not self.reference_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.reference_number = f"ISS-{self.company.company_type}-{timestamp}"
        super().save(*args, **kwargs)


class IssuePhoto(BaseModel):
    """Photos documenting the issue"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='photos')
    
    photo = models.ImageField(upload_to='issues/photos/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='issues/thumbnails/%Y/%m/%d/', blank=True)
    caption = models.CharField(max_length=500, blank=True)
    
    # Photo type
    PHOTO_TYPES = [
        ('BEFORE', 'Before'),
        ('AFTER', 'After'),
        ('EVIDENCE', 'Evidence'),
        ('OTHER', 'Other'),
    ]
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPES, default='EVIDENCE')
    
    taken_at = models.DateTimeField(auto_now_add=True)
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    sequence_number = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sequence_number', 'created_at']
    
    def __str__(self):
        return f"Photo {self.sequence_number} - {self.issue.reference_number}"


class IssueComment(BaseModel):
    """Comments and updates on issues"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    comment = models.TextField()
    is_internal = models.BooleanField(default=True)  # Internal vs customer-visible
    
    # Attachments
    has_attachments = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user} on {self.issue.reference_number}"


class IssueAttachment(BaseModel):
    """File attachments for issue comments"""
    comment = models.ForeignKey(IssueComment, on_delete=models.CASCADE, related_name='attachments')
    
    file = models.FileField(upload_to='issues/attachments/%Y/%m/%d/')
    file_name = models.CharField(max_length=200)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    file_type = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.file_name


class IssueTask(BaseModel):
    """Tasks required to resolve an issue"""
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='tasks')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='issue_tasks')
    
    # Dates
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_issue_tasks')
    
    # Order
    sequence = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sequence', 'created_at']
    
    def __str__(self):
        return f"{self.issue.reference_number} - Task: {self.title}"


class IssueHistory(models.Model):
    """Track all changes to an issue"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Change information
    action = models.CharField(max_length=50)  # created, updated, status_changed, etc.
    field_name = models.CharField(max_length=100, blank=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    
    # Metadata
    changed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'Issue Histories'
    
    def __str__(self):
        return f"{self.issue.reference_number} - {self.action} by {self.user}"


class IssueTemplate(BaseModel):
    """Templates for common issues"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='issue_templates')
    category = models.ForeignKey(IssueCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=200)
    description_template = models.TextField()
    
    # Defaults
    default_priority = models.CharField(max_length=20, default='MEDIUM')
    default_severity = models.CharField(max_length=20, default='MODERATE')
    default_assigned_team = models.CharField(max_length=100, blank=True)
    
    # Checklist
    checklist_items = models.JSONField(default=list, blank=True)
    
    # Usage
    usage_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-usage_count', 'name']
    
    def __str__(self):
        return self.name
