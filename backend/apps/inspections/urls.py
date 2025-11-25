"""
URL configuration for Inspections app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InspectionTypeViewSet, InspectionViewSet, InspectionPhotoViewSet,
    InspectionVideoViewSet, InspectionDocumentViewSet, InspectionTagViewSet,
    InspectionSignatureViewSet, InspectionCommentViewSet, ScannedReferenceViewSet,
    ContainerStructureViewSet, DamageTypeViewSet, StructureInspectionItemViewSet,
    InspectionChecklistViewSet
)

router = DefaultRouter()

# Main inspection resources
router.register(r'types', InspectionTypeViewSet, basename='inspection-type')
router.register(r'inspections', InspectionViewSet, basename='inspection')
router.register(r'photos', InspectionPhotoViewSet, basename='inspection-photo')
router.register(r'videos', InspectionVideoViewSet, basename='inspection-video')
router.register(r'documents', InspectionDocumentViewSet, basename='inspection-document')
router.register(r'tags', InspectionTagViewSet, basename='inspection-tag')
router.register(r'signatures', InspectionSignatureViewSet, basename='inspection-signature')
router.register(r'comments', InspectionCommentViewSet, basename='inspection-comment')
router.register(r'scanned-references', ScannedReferenceViewSet, basename='scanned-reference')

# Structure and damage resources
router.register(r'structures', ContainerStructureViewSet, basename='container-structure')
router.register(r'damage-types', DamageTypeViewSet, basename='damage-type')
router.register(r'structure-items', StructureInspectionItemViewSet, basename='structure-item')
router.register(r'checklists', InspectionChecklistViewSet, basename='inspection-checklist')

urlpatterns = [
    path('', include(router.urls)),
]
