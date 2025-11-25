"""
Models for Analytics app
Dashboard metrics and statistics
"""
from django.db import models
from apps.core.models import Company, User, BaseModel


class DashboardMetric(BaseModel):
    """Stored metrics for dashboard"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='metrics')
    
    metric_type = models.CharField(max_length=50)  # inspections_total, issues_open, etc.
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    metric_data = models.JSONField(default=dict, blank=True)  # Additional data
    
    period_start = models.DateField()
    period_end = models.DateField()
    
    class Meta:
        ordering = ['-period_end']
        indexes = [
            models.Index(fields=['company', 'metric_type', 'period_end']),
        ]
    
    def __str__(self):
        return f"{self.metric_type}: {self.metric_value}"
