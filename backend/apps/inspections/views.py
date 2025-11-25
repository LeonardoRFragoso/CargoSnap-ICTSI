"""
Views for Inspections app
Complete ViewSets for all inspection-related models
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import (
    IsAuthenticated, IsSameCompany, CanCreateInspection,
    CanEditInspection, CanDeleteInspection, IsAdminOrManager
)
from .models import (
    InspectionType, Inspection, InspectionPhoto, InspectionVideo,
    InspectionDocument, InspectionTag, InspectionSignature,
    InspectionComment, ScannedReference
)
from .structure_models import (
    ContainerStructure, DamageType, StructureInspectionItem,
    InspectionChecklist
)
from .serializers import (
    InspectionTypeSerializer, InspectionListSerializer,
    InspectionDetailSerializer, InspectionCreateUpdateSerializer,
    InspectionPhotoSerializer, InspectionVideoSerializer,
    InspectionDocumentSerializer, InspectionTagSerializer,
    InspectionSignatureSerializer, InspectionCommentSerializer,
    ScannedReferenceSerializer, ContainerStructureSerializer,
    DamageTypeSerializer, StructureInspectionItemSerializer,
    InspectionChecklistSerializer
)


class InspectionTypeViewSet(viewsets.ModelViewSet):
    """CRUD for Inspection Types"""
    queryset = InspectionType.objects.all()
    serializer_class = InspectionTypeSerializer
    permission_classes = [IsAuthenticated, IsSameCompany]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'is_active']
    search_fields = ['name', 'code']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)


class InspectionViewSet(viewsets.ModelViewSet):
    """CRUD for Inspections with multiple serializers"""
    queryset = Inspection.objects.all()
    permission_classes = [IsAuthenticated, IsSameCompany, CanCreateInspection]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'inspection_type', 'assigned_to', 'inspector']
    search_fields = ['reference_number', 'title', 'customer_name']
    ordering_fields = ['created_at', 'scheduled_date', 'completed_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = self.queryset.filter(company=self.request.user.company)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InspectionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return InspectionCreateUpdateSerializer
        return InspectionDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start an inspection"""
        from django.utils import timezone
        inspection = self.get_object()
        inspection.status = 'IN_PROGRESS'
        inspection.started_at = timezone.now()
        inspection.inspector = request.user
        inspection.save()
        return Response({'status': 'Inspection started'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete an inspection"""
        from django.utils import timezone
        inspection = self.get_object()
        inspection.status = 'COMPLETED'
        inspection.completed_at = timezone.now()
        inspection.save()
        return Response({'status': 'Inspection completed'})
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get inspection summary"""
        inspection = self.get_object()
        return Response({
            'reference': inspection.reference_number,
            'status': inspection.status,
            'photos': inspection.photos.count(),
            'videos': inspection.videos.count(),
            'documents': inspection.documents.count(),
            'comments': inspection.comments.count(),
            'issues': inspection.issues.count() if hasattr(inspection, 'issues') else 0,
        })


class InspectionPhotoViewSet(viewsets.ModelViewSet):
    """CRUD for Inspection Photos"""
    queryset = InspectionPhoto.objects.all()
    serializer_class = InspectionPhotoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inspection']
    
    def get_queryset(self):
        return self.queryset.filter(inspection__company=self.request.user.company)


class InspectionVideoViewSet(viewsets.ModelViewSet):
    """CRUD for Inspection Videos"""
    queryset = InspectionVideo.objects.all()
    serializer_class = InspectionVideoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inspection']
    
    def get_queryset(self):
        return self.queryset.filter(inspection__company=self.request.user.company)


class InspectionDocumentViewSet(viewsets.ModelViewSet):
    """CRUD for Inspection Documents"""
    queryset = InspectionDocument.objects.all()
    serializer_class = InspectionDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inspection', 'document_type']
    
    def get_queryset(self):
        return self.queryset.filter(inspection__company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class InspectionTagViewSet(viewsets.ModelViewSet):
    """CRUD for Tags"""
    queryset = InspectionTag.objects.all()
    serializer_class = InspectionTagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class InspectionSignatureViewSet(viewsets.ModelViewSet):
    """CRUD for Signatures"""
    queryset = InspectionSignature.objects.all()
    serializer_class = InspectionSignatureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inspection', 'signature_type']
    
    def get_queryset(self):
        return self.queryset.filter(inspection__company=self.request.user.company)


class InspectionCommentViewSet(viewsets.ModelViewSet):
    """CRUD for Comments"""
    queryset = InspectionComment.objects.all()
    serializer_class = InspectionCommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inspection', 'is_internal']
    
    def get_queryset(self):
        queryset = self.queryset.filter(inspection__company=self.request.user.company)
        # Clients can't see internal comments
        if self.request.user.role == 'CLIENT':
            queryset = queryset.filter(is_internal=False)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScannedReferenceViewSet(viewsets.ModelViewSet):
    """CRUD for Scanned References"""
    queryset = ScannedReference.objects.all()
    serializer_class = ScannedReferenceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inspection', 'reference_type', 'is_valid']
    
    def get_queryset(self):
        return self.queryset.filter(inspection__company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(scanned_by=self.request.user)


# Structure and Damage ViewSets

class ContainerStructureViewSet(viewsets.ModelViewSet):
    """CRUD for Container Structures"""
    queryset = ContainerStructure.objects.all()
    serializer_class = ContainerStructureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['group', 'is_critical', 'is_active']
    search_fields = ['name', 'code']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)


class DamageTypeViewSet(viewsets.ModelViewSet):
    """CRUD for Damage Types"""
    queryset = DamageType.objects.all()
    serializer_class = DamageTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['default_severity', 'affects_operation', 'is_active']
    search_fields = ['name', 'code']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)


class StructureInspectionItemViewSet(viewsets.ModelViewSet):
    """CRUD for Structure Inspection Items"""
    queryset = StructureInspectionItem.objects.all()
    serializer_class = StructureInspectionItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['inspection', 'structure', 'status', 'damage_type']
    
    def get_queryset(self):
        return self.queryset.filter(inspection__company=self.request.user.company)
    
    def perform_create(self, serializer):
        from django.utils import timezone
        serializer.save(
            inspected_by=self.request.user,
            inspected_at=timezone.now()
        )


class InspectionChecklistViewSet(viewsets.ModelViewSet):
    """CRUD for Inspection Checklists"""
    queryset = InspectionChecklist.objects.all()
    serializer_class = InspectionChecklistSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['container_type', 'is_active', 'is_default']
    search_fields = ['name']
    
    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.company)
    
    def perform_create(self, serializer):
        serializer.save(
            company=self.request.user.company,
            created_by=self.request.user
        )
