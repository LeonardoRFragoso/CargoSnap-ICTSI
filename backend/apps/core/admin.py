"""
Admin configuration for Core app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Company, User, AuditLog, Notification, 
    Webhook, WebhookLog, ApiKey
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_type', 'city', 'state', 'is_active', 'created_at']
    list_filter = ['company_type', 'is_active', 'state']
    search_fields = ['name', 'email', 'city']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Informações Básicas'), {
            'fields': ('name', 'slug', 'company_type', 'logo', 'is_active')
        }),
        (_('Contato'), {
            'fields': ('email', 'phone', 'website')
        }),
        (_('Endereço'), {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        (_('Personalização'), {
            'fields': ('primary_color', 'secondary_color')
        }),
        (_('Datas'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'company', 'role', 'is_active']
    list_filter = ['company', 'role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']
    
    fieldsets = (
        (_('Informações de Login'), {
            'fields': ('username', 'password')
        }),
        (_('Informações Pessoais'), {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar')
        }),
        (_('Empresa e Função'), {
            'fields': ('company', 'role')
        }),
        (_('Configurações'), {
            'fields': ('language', 'timezone')
        }),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Datas'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'company', 'role'),
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'action', 'model_name', 'object_id', 'created_at']
    list_filter = ['company', 'action', 'model_name', 'created_at']
    search_fields = ['user__username', 'user__email', 'object_id', 'description']
    readonly_fields = ['user', 'company', 'action', 'model_name', 'object_id', 
                      'description', 'ip_address', 'user_agent', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'company', 'notification_type', 'channel', 'is_read', 'created_at']
    list_filter = ['company', 'notification_type', 'channel', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'sent_at']


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'event_type', 'url', 'is_active', 'total_calls', 'successful_calls', 'failed_calls']
    list_filter = ['company', 'event_type', 'is_active']
    search_fields = ['name', 'url', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_calls', 'successful_calls', 'failed_calls', 'last_called_at', 'last_status_code']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'name', 'description', 'url', 'event_type')
        }),
        ('Security', {
            'fields': ('secret_key', 'is_active', 'custom_headers')
        }),
        ('Retry Configuration', {
            'fields': ('retry_on_failure', 'max_retries')
        }),
        ('Statistics', {
            'fields': ('total_calls', 'successful_calls', 'failed_calls', 'last_called_at', 'last_status_code'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ['webhook', 'status_code', 'success', 'attempt_number', 'response_time_ms', 'called_at']
    list_filter = ['success', 'webhook', 'called_at']
    search_fields = ['webhook__name', 'error_message']
    readonly_fields = ['webhook', 'payload', 'headers', 'status_code', 'response_body', 
                      'response_time_ms', 'success', 'error_message', 'attempt_number', 'called_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'user', 'is_active', 'last_used_at', 'total_requests', 'created_at']
    list_filter = ['company', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'key']
    readonly_fields = ['key', 'created_at', 'updated_at', 'last_used_at', 'total_requests']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'user', 'name', 'description', 'key')
        }),
        ('Permissions & Limits', {
            'fields': ('permissions', 'rate_limit_per_hour')
        }),
        ('Status', {
            'fields': ('is_active', 'expires_at')
        }),
        ('Usage Statistics', {
            'fields': ('last_used_at', 'total_requests'),
            'classes': ('collapse',)
        }),
    )
