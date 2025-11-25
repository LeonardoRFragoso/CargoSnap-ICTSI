"""
Middleware for multi-tenant system
Ensures data isolation between companies
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to set the current company based on authenticated user
    Ensures all database queries are filtered by company
    """
    
    def process_request(self, request):
        """
        Add company to request if user is authenticated
        """
        if hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request.user, 'company'):
                request.company = request.user.company
            else:
                # Superuser without company - allow access
                request.company = None
        else:
            request.company = None
        
        return None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Validate company access for API views
        """
        # Skip validation for admin, auth, and public endpoints
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/api/auth/') or
            request.path.startswith('/api/schema/') or
            request.path.startswith('/api/docs/')):
            return None
        
        # Check if user has company access
        if hasattr(request, 'user') and request.user.is_authenticated:
            if not request.user.is_superuser and not hasattr(request.user, 'company'):
                return JsonResponse(
                    {'error': 'Usuário não está associado a nenhuma empresa'},
                    status=403
                )
            
            if hasattr(request.user, 'company') and not request.user.company.is_active:
                return JsonResponse(
                    {'error': 'Empresa desativada'},
                    status=403
                )
        
        return None
