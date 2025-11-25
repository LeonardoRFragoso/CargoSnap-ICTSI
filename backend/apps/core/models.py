"""
Core models for CargoSnap ICTSI
Multi-tenant system with Company and User models
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    """
    Company model for multi-tenant system
    Supports: ICTSI, iTracker, CLIA
    """
    COMPANY_TYPES = [
        ('ICTSI', 'ICTSI - International Container Terminal Services'),
        ('ITRACKER', 'iTracker - Sistema de Rastreamento'),
        ('CLIA', 'CLIA - Centro Logístico e Industrial de Aratu'),
    ]
    
    name = models.CharField(_('Nome'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    company_type = models.CharField(_('Tipo'), max_length=20, choices=COMPANY_TYPES)
    
    # Contact Information
    email = models.EmailField(_('E-mail'), blank=True)
    phone = models.CharField(_('Telefone'), max_length=20, blank=True)
    website = models.URLField(_('Website'), blank=True)
    
    # Address
    address = models.CharField(_('Endereço'), max_length=255, blank=True)
    city = models.CharField(_('Cidade'), max_length=100, blank=True)
    state = models.CharField(_('Estado'), max_length=2, blank=True)
    zip_code = models.CharField(_('CEP'), max_length=10, blank=True)
    country = models.CharField(_('País'), max_length=100, default='Brasil')
    
    # Settings
    logo = models.ImageField(_('Logo'), upload_to='companies/logos/', blank=True, null=True)
    primary_color = models.CharField(_('Cor Primária'), max_length=7, default='#1E40AF')
    secondary_color = models.CharField(_('Cor Secundária'), max_length=7, default='#3B82F6')
    
    # Status
    is_active = models.BooleanField(_('Ativo'), default=True)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom User model with company association
    Each user belongs to one company
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('MANAGER', 'Gerente'),
        ('INSPECTOR', 'Inspetor'),
        ('VIEWER', 'Visualizador'),
    ]
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name=_('Empresa')
    )
    
    role = models.CharField(
        _('Função'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='INSPECTOR'
    )
    
    # Additional fields
    phone = models.CharField(_('Telefone'), max_length=20, blank=True)
    avatar = models.ImageField(_('Avatar'), upload_to='users/avatars/', blank=True, null=True)
    
    # Settings
    language = models.CharField(_('Idioma'), max_length=10, default='pt-br')
    timezone = models.CharField(_('Fuso Horário'), max_length=50, default='America/Sao_Paulo')
    
    # Status
    is_active = models.BooleanField(_('Ativo'), default=True)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        ordering = ['company', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.company.name})"
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_manager(self):
        return self.role in ['ADMIN', 'MANAGER']
    
    @property
    def can_create_inspections(self):
        return self.role in ['ADMIN', 'MANAGER', 'INSPECTOR']


class AuditLog(models.Model):
    """
    Audit log for tracking user actions
    """
    ACTION_TYPES = [
        ('CREATE', 'Criação'),
        ('UPDATE', 'Atualização'),
        ('DELETE', 'Exclusão'),
        ('VIEW', 'Visualização'),
        ('EXPORT', 'Exportação'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name=_('Usuário')
    )
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='audit_logs',
        verbose_name=_('Empresa')
    )
    
    action = models.CharField(_('Ação'), max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(_('Modelo'), max_length=100)
    object_id = models.CharField(_('ID do Objeto'), max_length=100)
    description = models.TextField(_('Descrição'), blank=True)
    
    ip_address = models.GenericIPAddressField(_('Endereço IP'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Log de Auditoria')
        verbose_name_plural = _('Logs de Auditoria')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} ({self.created_at})"


class BaseModel(models.Model):
    """Abstract base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Notification(BaseModel):
    """System notifications for users"""
    NOTIFICATION_TYPES = [
        ('INFO', 'Information'),
        ('SUCCESS', 'Success'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('TASK', 'Task Assignment'),
        ('MENTION', 'Mention'),
        ('REMINDER', 'Reminder'),
    ]
    
    CHANNELS = [
        ('IN_APP', 'In-App'),
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push Notification'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Notification content
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='INFO')
    
    # Delivery
    channel = models.CharField(max_length=20, choices=CHANNELS, default='IN_APP')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Action link
    action_url = models.URLField(blank=True)
    action_text = models.CharField(max_length=100, blank=True)
    
    # Related object (generic relation could be used here)
    related_model = models.CharField(max_length=100, blank=True)
    related_id = models.CharField(max_length=100, blank=True)
    
    # Metadata
    data = models.JSONField(default=dict, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['company', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class Webhook(BaseModel):
    """Webhook configurations for external integrations"""
    EVENT_TYPES = [
        ('inspection.created', 'Inspection Created'),
        ('inspection.updated', 'Inspection Updated'),
        ('inspection.completed', 'Inspection Completed'),
        ('inspection.approved', 'Inspection Approved'),
        ('issue.created', 'Issue Created'),
        ('issue.resolved', 'Issue Resolved'),
        ('report.generated', 'Report Generated'),
        ('workflow.completed', 'Workflow Completed'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='webhooks')
    
    # Webhook configuration
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    
    # Security
    secret_key = models.CharField(max_length=200, blank=True)  # For signing payloads
    is_active = models.BooleanField(default=True)
    
    # Headers (JSON)
    custom_headers = models.JSONField(default=dict, blank=True)
    
    # Retry configuration
    retry_on_failure = models.BooleanField(default=True)
    max_retries = models.IntegerField(default=3)
    
    # Statistics
    total_calls = models.IntegerField(default=0)
    successful_calls = models.IntegerField(default=0)
    failed_calls = models.IntegerField(default=0)
    last_called_at = models.DateTimeField(null=True, blank=True)
    last_status_code = models.IntegerField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_webhooks')
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['company', 'event_type', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.event_type}"


class WebhookLog(models.Model):
    """Log of webhook calls"""
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='logs')
    
    # Request
    payload = models.JSONField()
    headers = models.JSONField(default=dict)
    
    # Response
    status_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    response_time_ms = models.IntegerField(default=0)
    
    # Status
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    # Retry
    attempt_number = models.IntegerField(default=1)
    
    # Timing
    called_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-called_at']
        indexes = [
            models.Index(fields=['webhook', 'success']),
            models.Index(fields=['called_at']),
        ]
    
    def __str__(self):
        return f"{self.webhook.name} - {self.status_code} - {self.called_at}"


class ApiKey(BaseModel):
    """API Keys for external integrations"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='api_keys')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    
    # Key information
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Permissions
    permissions = models.JSONField(default=list, blank=True)  # List of allowed operations
    
    # Limits
    rate_limit_per_hour = models.IntegerField(default=1000)
    
    # Status
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Usage statistics
    last_used_at = models.DateTimeField(null=True, blank=True)
    total_requests = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['company', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate key if not provided
        if not self.key:
            import secrets
            self.key = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
