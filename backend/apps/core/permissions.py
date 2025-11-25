"""
Custom permissions for multi-tenant system
"""
from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """
    Only authenticated users can access
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsSameCompany(permissions.BasePermission):
    """
    User can only access resources from their own company (multi-tenant)
    """
    def has_object_permission(self, request, view, obj):
        # Check if object has company attribute
        if hasattr(obj, 'company'):
            return obj.company == request.user.company
        return False


class IsAdminOrManager(permissions.BasePermission):
    """
    Only Admin or Manager roles can perform action
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['ADMIN', 'MANAGER']
        )


class IsAdmin(permissions.BasePermission):
    """
    Only Admin role can perform action
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )


class CanCreateInspection(permissions.BasePermission):
    """
    User can create inspections (Admin, Manager, Inspector)
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['ADMIN', 'MANAGER', 'INSPECTOR']
            )
        return True


class CanEditInspection(permissions.BasePermission):
    """
    User can edit inspections (Admin, Manager, or assigned Inspector)
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            # Admin and Manager can edit any
            if request.user.role in ['ADMIN', 'MANAGER']:
                return True
            # Inspector can edit if assigned
            if request.user.role == 'INSPECTOR':
                return obj.assigned_to == request.user or obj.inspector == request.user
        return True


class CanDeleteInspection(permissions.BasePermission):
    """
    Only Admin and Manager can delete inspections
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.role in ['ADMIN', 'MANAGER']
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    User can only edit/delete their own objects
    Read-only for others
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False


class IsAssignedOrReadOnly(permissions.BasePermission):
    """
    User can edit if assigned to them, read-only otherwise
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions for assigned user or managers
        if request.user.role in ['ADMIN', 'MANAGER']:
            return True
        
        if hasattr(obj, 'assigned_to'):
            return obj.assigned_to == request.user
        
        return False


class CanViewInternalComments(permissions.BasePermission):
    """
    Only company employees can view internal comments
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'is_internal') and obj.is_internal:
            return request.user.role != 'CLIENT'
        return True


class CanManageWebhooks(permissions.BasePermission):
    """
    Only Admin can manage webhooks
    """
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.role == 'ADMIN'
        return True


class CanGenerateReports(permissions.BasePermission):
    """
    Admin, Manager, and Inspector can generate reports
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['ADMIN', 'MANAGER', 'INSPECTOR']
        )


class ReadOnlyOrCreate(permissions.BasePermission):
    """
    Read-only or create only (no edit/delete)
    Useful for audit logs
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        return False
