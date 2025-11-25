from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
import logging

from .models import (
    CargoSnapFile, CargoSnapUpload, CargoSnapWorkflow,
    CargoSnapSyncLog
)
from .serializers import (
    CargoSnapFileListSerializer, CargoSnapFileDetailSerializer,
    CargoSnapUploadSerializer, CargoSnapWorkflowSerializer,
    CargoSnapSyncLogSerializer, CargoSnapStatsSerializer
)
from .services import CargoSnapAPIService
from .integration_services import CargoSnapInspectionIntegrator

logger = logging.getLogger(__name__)


class CargoSnapFileViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para arquivos do CargoSnap"""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['closed', 'sync_status']
    search_fields = ['scan_code', 'cargosnap_id']
    ordering_fields = ['created_at', 'updated_at', 'scan_code', 'snap_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = CargoSnapFile.objects.all()
        
        # Filtro por dano
        has_damage = self.request.query_params.get('has_damage')
        if has_damage is not None:
            if has_damage.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(snap_count_with_damage__gt=0)
            else:
                queryset = queryset.filter(snap_count_with_damage=0)
        
        # Filtro por data
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CargoSnapFileDetailSerializer
        return CargoSnapFileListSerializer
    
    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """Sincroniza um arquivo específico"""
        file_obj = self.get_object()
        
        try:
            service = CargoSnapAPIService()
            details = service.get_file_details(file_obj.cargosnap_id)
            service.sync_file_details(file_obj, details)
            
            # Download de imagens se solicitado
            download_images = request.data.get('download_images', True)
            if download_images:
                downloaded, failed = service.download_file_images(file_obj)
                return Response({
                    'status': 'success',
                    'message': 'Arquivo sincronizado com sucesso',
                    'images_downloaded': downloaded,
                    'images_failed': failed
                })
            
            return Response({
                'status': 'success',
                'message': 'Arquivo sincronizado com sucesso'
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def download_images(self, request, pk=None):
        """Baixa imagens de um arquivo específico"""
        file_obj = self.get_object()
        
        try:
            service = CargoSnapAPIService()
            downloaded, failed = service.download_file_images(file_obj)
            
            return Response({
                'status': 'success',
                'images_downloaded': downloaded,
                'images_failed': failed
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Retorna estatísticas gerais"""
        
        total_files = CargoSnapFile.objects.count()
        total_images = CargoSnapUpload.objects.count()
        images_downloaded = CargoSnapUpload.objects.filter(image_downloaded=True).count()
        images_pending = total_images - images_downloaded
        files_with_damage = CargoSnapFile.objects.filter(snap_count_with_damage__gt=0).count()
        total_damage_images = CargoSnapUpload.objects.filter(has_damage=True).count()
        
        # Última sincronização
        last_sync_log = CargoSnapSyncLog.objects.filter(status='completed').order_by('-finished_at').first()
        last_sync = last_sync_log.finished_at if last_sync_log else None
        
        # Status de sincronização
        sync_status = dict(
            CargoSnapFile.objects.values_list('sync_status').annotate(count=Count('id'))
        )
        
        data = {
            'total_files': total_files,
            'total_images': total_images,
            'images_downloaded': images_downloaded,
            'images_pending': images_pending,
            'files_with_damage': files_with_damage,
            'total_damage_images': total_damage_images,
            'last_sync': last_sync,
            'sync_status': sync_status
        }
        
        serializer = CargoSnapStatsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def create_inspection(self, request, pk=None):
        """
        Cria uma inspeção ICTSI a partir deste arquivo CargoSnap
        
        Body params:
            - company_id: ID da empresa
            - inspection_type_id: ID do tipo de inspeção
            - assigned_to_id: ID do usuário responsável (opcional)
            - import_photos: Boolean para importar fotos (default: True)
        """
        file_obj = self.get_object()
        
        try:
            from apps.inspections.models import InspectionType
            from apps.core.models import Company, User
            
            company_id = request.data.get('company_id')
            inspection_type_id = request.data.get('inspection_type_id')
            assigned_to_id = request.data.get('assigned_to_id')
            import_photos = request.data.get('import_photos', True)
            
            if not company_id or not inspection_type_id:
                return Response({
                    'error': 'company_id e inspection_type_id são obrigatórios'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            company = Company.objects.get(id=company_id)
            inspection_type = InspectionType.objects.get(id=inspection_type_id)
            assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None
            
            integrator = CargoSnapInspectionIntegrator()
            inspection = integrator.create_inspection_from_cargosnap(
                cargosnap_file=file_obj,
                company=company,
                inspection_type=inspection_type,
                assigned_to=assigned_to,
                import_photos=import_photos
            )
            
            from apps.inspections.serializers import InspectionSerializer
            return Response({
                'status': 'success',
                'message': f'Inspeção {inspection.reference_number} criada com sucesso',
                'inspection': InspectionSerializer(inspection).data
            }, status=status.HTTP_201_CREATED)
            
        except (Company.DoesNotExist, InspectionType.DoesNotExist, User.DoesNotExist) as e:
            return Response({
                'error': f'Recurso não encontrado: {str(e)}'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Erro ao criar inspeção: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def unified_search(self, request):
        """
        Busca unificada por número de container (CargoSnap + Inspeções)
        
        Query params:
            - container: Número do container
        """
        container_number = request.query_params.get('container')
        
        if not container_number:
            return Response({
                'error': 'Parâmetro "container" é obrigatório'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            integrator = CargoSnapInspectionIntegrator()
            unified_data = integrator.get_container_unified_data(container_number)
            
            return Response(unified_data)
            
        except Exception as e:
            logger.error(f"Erro na busca unificada: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def auto_link_inspections(self, request):
        """
        Vincula automaticamente inspeções existentes com arquivos CargoSnap
        baseado no número do container
        """
        try:
            integrator = CargoSnapInspectionIntegrator()
            stats = integrator.auto_link_by_container_number()
            
            return Response({
                'status': 'success',
                'message': 'Vinculação automática concluída',
                'stats': stats
            })
            
        except Exception as e:
            logger.error(f"Erro na vinculação automática: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CargoSnapUploadViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para uploads (imagens) do CargoSnap"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = CargoSnapUploadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['has_damage', 'image_downloaded', 'file']
    search_fields = ['file__scan_code', 'device_nick', 'workflow_step_description']
    ordering_fields = ['scan_date_time', 'created_at']
    ordering = ['-scan_date_time']
    
    def get_queryset(self):
        queryset = CargoSnapUpload.objects.select_related('file').all()
        
        # Filtro por arquivo
        file_id = self.request.query_params.get('file_id')
        if file_id:
            queryset = queryset.filter(file_id=file_id)
        
        # Filtro por workflow
        workflow_id = self.request.query_params.get('workflow_id')
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        
        # Filtro por data
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(scan_date_time__gte=date_from)
        if date_to:
            queryset = queryset.filter(scan_date_time__lte=date_to)
        
        return queryset


class CargoSnapWorkflowViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para workflows do CargoSnap"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = CargoSnapWorkflowSerializer
    queryset = CargoSnapWorkflow.objects.prefetch_related('steps').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'cargosnap_id']
    ordering_fields = ['order', 'name', 'created_at']
    ordering = ['order', 'name']


class CargoSnapSyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para logs de sincronização"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = CargoSnapSyncLogSerializer
    queryset = CargoSnapSyncLog.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['started_at', 'finished_at']
    ordering = ['-started_at']
    
    @action(detail=False, methods=['post'])
    def trigger_sync(self, request):
        """Inicia uma nova sincronização"""
        
        logger.info("="*60)
        logger.info("🚀 TRIGGER_SYNC CHAMADO!")
        logger.info("="*60)
        logger.info(f"User: {request.user}")
        logger.info(f"Data: {request.data}")
        
        download_images = request.data.get('download_images', True)
        logger.info(f"Download images: {download_images}")
        
        try:
            logger.info("Criando instância do CargoSnapAPIService...")
            service = CargoSnapAPIService()
            
            # Executa sincronização em background (idealmente usar Celery)
            # Por enquanto, execução síncrona
            logger.info("Iniciando full_sync...")
            sync_log = service.full_sync(download_images=download_images)
            
            logger.info(f"✅ Sincronização concluída! ID: {sync_log.id}")
            
            serializer = self.get_serializer(sync_log)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"❌ ERRO na sincronização: {str(e)}")
            logger.exception(e)
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
