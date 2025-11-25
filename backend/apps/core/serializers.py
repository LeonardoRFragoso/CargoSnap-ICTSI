"""
Serializers for Core app
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Company, User, AuditLog, Notification, Webhook, WebhookLog, ApiKey


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model"""
    
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'slug', 'company_type', 'email', 'phone', 'website',
            'address', 'city', 'state', 'zip_code', 'country',
            'logo', 'primary_color', 'secondary_color',
            'is_active', 'user_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_count(self, obj):
        return obj.users.filter(is_active=True).count()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    company_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'company', 'company_name', 'role', 'phone', 'avatar',
            'language', 'timezone', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_company_name(self, obj):
        return obj.company.name if obj.company else None
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users"""
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'company', 'role', 'phone'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone', 'avatar',
            'language', 'timezone'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "As senhas não coincidem."})
        return attrs


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for Audit Log"""
    
    user_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_name', 'company', 'company_name',
            'action', 'model_name', 'object_id', 'description',
            'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None
    
    def get_company_name(self, obj):
        return obj.company.name if obj.company else None


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notifications"""
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'company', 'user', 'user_name', 'title', 'message', 'notification_type',
            'channel', 'is_read', 'read_at', 'action_url', 'action_text',
            'related_model', 'related_id', 'data', 'sent_at', 'created_at'
        ]
        read_only_fields = ['user', 'read_at', 'sent_at', 'created_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else obj.user.username if obj.user else None


class WebhookLogSerializer(serializers.ModelSerializer):
    """Serializer for Webhook Logs"""
    webhook_name = serializers.CharField(source='webhook.name', read_only=True)
    
    class Meta:
        model = WebhookLog
        fields = [
            'id', 'webhook', 'webhook_name', 'payload', 'headers',
            'status_code', 'response_body', 'response_time_ms',
            'success', 'error_message', 'attempt_number', 'called_at'
        ]
        read_only_fields = ['called_at']


class WebhookSerializer(serializers.ModelSerializer):
    """Serializer for Webhooks"""
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Webhook
        fields = [
            'id', 'company', 'name', 'description', 'url', 'event_type',
            'secret_key', 'is_active', 'custom_headers', 'retry_on_failure',
            'max_retries', 'total_calls', 'successful_calls', 'failed_calls',
            'last_called_at', 'last_status_code', 'created_by',
            'success_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_calls', 'successful_calls', 'failed_calls',
                           'last_called_at', 'last_status_code', 'created_by',
                           'created_at', 'updated_at']
    
    def get_success_rate(self, obj):
        if obj.total_calls == 0:
            return 0
        return round((obj.successful_calls / obj.total_calls) * 100, 2)


class ApiKeySerializer(serializers.ModelSerializer):
    """Serializer for API Keys"""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = ApiKey
        fields = [
            'id', 'company', 'company_name', 'user', 'user_name',
            'name', 'key', 'description', 'permissions', 'rate_limit_per_hour',
            'is_active', 'expires_at', 'last_used_at', 'total_requests',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['key', 'last_used_at', 'total_requests', 'created_at', 'updated_at']
