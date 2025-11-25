"""
Mixins for views and viewsets
"""
from rest_framework import viewsets


class CompanyFilterMixin:
    """
    Mixin to filter querysets by company.
    Superusers see all data, regular users see only their company's data.
    """
    
    def filter_by_company(self, queryset, company_field='company'):
        """
        Filter queryset by company field.
        
        Args:
            queryset: The base queryset to filter
            company_field: The field name that references company (default: 'company')
                          For related fields, use '__' notation (e.g., 'inspection__company')
        
        Returns:
            Filtered queryset
        """
        if self.request.user.is_superuser:
            return queryset
        
        if self.request.user.company is None:
            # User without company (shouldn't happen for non-superusers)
            return queryset.none()
        
        filter_kwargs = {company_field: self.request.user.company}
        return queryset.filter(**filter_kwargs)
    
    def get_user_company(self):
        """
        Get the user's company, or None for superusers.
        
        Returns:
            Company instance or None
        """
        if self.request.user.is_superuser:
            return None
        return self.request.user.company
