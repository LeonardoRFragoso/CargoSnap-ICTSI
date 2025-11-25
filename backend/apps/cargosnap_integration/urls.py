from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CargoSnapFileViewSet, CargoSnapUploadViewSet,
    CargoSnapWorkflowViewSet, CargoSnapSyncLogViewSet
)

app_name = 'cargosnap_integration'

router = DefaultRouter()
router.register(r'files', CargoSnapFileViewSet, basename='cargosnap-file')
router.register(r'uploads', CargoSnapUploadViewSet, basename='cargosnap-upload')
router.register(r'workflows', CargoSnapWorkflowViewSet, basename='cargosnap-workflow')
router.register(r'sync-logs', CargoSnapSyncLogViewSet, basename='cargosnap-synclog')

urlpatterns = [
    path('', include(router.urls)),
]
