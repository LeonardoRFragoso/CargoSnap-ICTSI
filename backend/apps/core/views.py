"""
Views for Core app - Authentication and User Management
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import update_session_auth_hash, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from .models import Company, User, AuditLog, Notification, Webhook, WebhookLog, ApiKey
from .serializers import (
    CompanySerializer, UserSerializer, UserCreateSerializer,
    UserUpdateSerializer, ChangePasswordSerializer, AuditLogSerializer,
    NotificationSerializer, WebhookSerializer, WebhookLogSerializer, ApiKeySerializer
)
from .permissions import IsAdminOrManager, CanManageWebhooks
from .forms import LoginForm, RegisterForm, PasswordResetRequestForm


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer with additional user data"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'full_name': self.user.get_full_name(),
            'role': self.user.role,
            'company': {
                'id': self.user.company.id,
                'name': self.user.company.name,
                'slug': self.user.company.slug,
                'company_type': self.user.company.company_type,
            }
        }
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view with user data"""
    serializer_class = CustomTokenObtainPairSerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for companies - Read only
    Only admins can view all companies
    """
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter companies based on user role"""
        user = self.request.user
        
        if user.is_superuser or user.is_admin:
            return Company.objects.all()
        
        # Regular users can only see their own company
        return Company.objects.filter(id=user.company.id)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management
    Users can only see and manage users from their own company
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter users by company"""
        user = self.request.user
        
        if user.is_superuser:
            return User.objects.all()
        
        # Users can only see users from their own company
        return User.objects.filter(company=user.company)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        """Ensure user is created in the correct company"""
        user = self.request.user
        
        # Non-admin users can only create users in their own company
        if not user.is_admin and serializer.validated_data.get('company') != user.company:
            serializer.validated_data['company'] = user.company
        
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change current user password"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': ['Senha incorreta.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        update_session_auth_hash(request, user)
        
        return Response({'message': 'Senha alterada com sucesso.'})


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for audit logs - Read only
    Users can only see logs from their own company
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['action', 'model_name', 'user']
    search_fields = ['description', 'object_id']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter logs by company"""
        user = self.request.user
        
        if user.is_superuser:
            return AuditLog.objects.all()
        
        # Users can only see logs from their own company
        return AuditLog.objects.filter(company=user.company)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['notification_type', 'channel', 'is_read']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'status': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        from django.utils import timezone
        self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({'status': 'All notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'count': count})


class WebhookViewSet(viewsets.ModelViewSet):
    """ViewSet for Webhooks"""
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageWebhooks]
    filterset_fields = ['event_type', 'is_active']
    search_fields = ['name', 'url']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test webhook with sample payload"""
        webhook = self.get_object()
        # TODO: Implement actual webhook call
        return Response({'status': 'Test webhook sent'})


class WebhookLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Webhook Logs - Read only"""
    queryset = WebhookLog.objects.all()
    serializer_class = WebhookLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['webhook', 'success']
    ordering = ['-called_at']
    
    def get_queryset(self):
        return self.queryset.filter(webhook__company=self.request.user.company)


class ApiKeyViewSet(viewsets.ModelViewSet):
    """ViewSet for API Keys"""
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]
    filterset_fields = ['is_active']
    search_fields = ['name']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            user=self.request.user
        )


# ============================================================================
# TRADITIONAL DJANGO VIEWS (for HTML templates)
# ============================================================================

def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.get_full_name()}!')
                return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def register_view(request):
    """Register page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    companies = Company.objects.filter(is_active=True)
    return render(request, 'auth/register.html', {'form': form, 'companies': companies})


def logout_view(request):
    """Logout"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


def password_reset_view(request):
    """Password reset request page"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            # TODO: Send password reset email
            messages.success(request, 'Instruções enviadas para seu email!')
            return redirect('password_reset_done')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'auth/password_reset.html', {'form': form})


def password_reset_done_view(request):
    """Password reset done page"""
    return render(request, 'auth/password_reset_done.html')


@login_required
def dashboard_view(request):
    """Dashboard page"""
    from apps.inspections.models import Inspection
    from apps.issues.models import Issue
    from django.db.models import Count
    
    company = request.user.company
    
    # Statistics
    inspections = Inspection.objects.filter(company=company)
    issues = Issue.objects.filter(company=company)
    
    stats = {
        'total_inspections': inspections.count(),
        'completed_inspections': inspections.filter(status='COMPLETED').count(),
        'in_progress_inspections': inspections.filter(status='IN_PROGRESS').count(),
        'draft_inspections': inspections.filter(status='DRAFT').count(),
        'total_issues': issues.count(),
        'open_issues': issues.filter(status='OPEN').count(),
        'resolved_issues': issues.filter(status='RESOLVED').count(),
    }
    
    # Recent inspections
    recent_inspections = inspections.order_by('-created_at')[:10]
    
    context = {
        'stats': stats,
        'recent_inspections': recent_inspections,
    }
    
    return render(request, 'dashboard/index.html', context)
