"""
Serviços de integração entre CargoSnap e sistema de Inspeções ICTSI
"""
from django.db import transaction
from django.core.files import File
from django.utils import timezone
from pathlib import Path
import logging
import shutil
from PIL import Image
from io import BytesIO

from .models import CargoSnapFile, CargoSnapUpload
from apps.inspections.models import Inspection, InspectionPhoto, InspectionType
from apps.core.models import Company

logger = logging.getLogger(__name__)


class CargoSnapInspectionIntegrator:
    """Integra dados do CargoSnap com Inspeções ICTSI"""
    
    @transaction.atomic
    def create_inspection_from_cargosnap(
        self,
        cargosnap_file: CargoSnapFile,
        company: Company,
        inspection_type: InspectionType,
        assigned_to=None,
        import_photos: bool = True
    ) -> Inspection:
        """
        Cria uma nova inspeção ICTSI a partir de um arquivo CargoSnap
        
        Args:
            cargosnap_file: Arquivo CargoSnap fonte
            company: Empresa responsável pela inspeção
            inspection_type: Tipo de inspeção
            assigned_to: Usuário responsável (opcional)
            import_photos: Se True, importa fotos do CargoSnap
            
        Returns:
            Inspeção criada
        """
        try:
            logger.info(f"Criando inspeção a partir do CargoSnap: {cargosnap_file.scan_code}")
            
            # Criar inspeção
            inspection = Inspection.objects.create(
                company=company,
                inspection_type=inspection_type,
                cargosnap_file=cargosnap_file,
                imported_from_cargosnap=True,
                container_number=cargosnap_file.scan_code,
                title=f"Inspeção Container {cargosnap_file.scan_code}",
                description=f"Inspeção importada do CargoSnap em {timezone.now().strftime('%d/%m/%Y %H:%M')}",
                status='IN_PROGRESS',
                assigned_to=assigned_to,
                started_at=cargosnap_file.created_at,
                metadata={
                    'cargosnap_id': cargosnap_file.cargosnap_id,
                    'total_snaps': cargosnap_file.snap_count,
                    'snaps_with_damage': cargosnap_file.snap_count_with_damage,
                    'imported_at': timezone.now().isoformat()
                }
            )
            
            logger.info(f"Inspeção criada: {inspection.reference_number}")
            
            # Importar fotos se solicitado
            if import_photos:
                imported_count = self._import_photos_from_cargosnap(inspection, cargosnap_file)
                logger.info(f"Importadas {imported_count} fotos do CargoSnap")
            
            return inspection
            
        except Exception as e:
            logger.error(f"Erro ao criar inspeção do CargoSnap: {str(e)}")
            raise
    
    def _import_photos_from_cargosnap(
        self,
        inspection: Inspection,
        cargosnap_file: CargoSnapFile
    ) -> int:
        """
        Importa fotos do CargoSnap para a inspeção
        
        Returns:
            Número de fotos importadas
        """
        imported_count = 0
        
        # Buscar apenas uploads com imagens baixadas localmente
        uploads = cargosnap_file.uploads.filter(
            image_downloaded=True,
            local_image_path__isnull=False
        ).order_by('scan_date_time')
        
        for sequence, upload in enumerate(uploads, start=1):
            try:
                # Copiar arquivo de imagem
                photo = self._copy_cargosnap_image_to_inspection(upload, inspection)
                
                if photo:
                    # Criar registro de foto na inspeção
                    InspectionPhoto.objects.create(
                        inspection=inspection,
                        photo=photo,
                        cargosnap_upload=upload,
                        photo_source='CARGOSNAP',
                        title=upload.workflow_step_description or f"Foto {sequence}",
                        description=upload.comment or '',
                        caption=f"Importada do CargoSnap - {upload.device_nick or 'Dispositivo'}",
                        latitude=self._parse_coordinate(upload.latitude),
                        longitude=self._parse_coordinate(upload.longitude),
                        taken_at=upload.scan_date_time,
                        sequence_number=sequence,
                        device_info={
                            'source': 'cargosnap',
                            'device_nick': upload.device_nick,
                            'device_id': upload.device_id,
                            'has_damage': upload.has_damage,
                            'damage_type': upload.damage_type_desc,
                        }
                    )
                    imported_count += 1
                    logger.info(f"Foto importada: {upload.cargosnap_id}")
                    
            except Exception as e:
                logger.error(f"Erro ao importar foto {upload.cargosnap_id}: {str(e)}")
                continue
        
        return imported_count
    
    def _copy_cargosnap_image_to_inspection(
        self,
        upload: CargoSnapUpload,
        inspection: Inspection
    ):
        """
        Copia imagem do CargoSnap para o diretório de inspeções
        
        Returns:
            Path relativo da imagem copiada ou None se falhar
        """
        try:
            from django.conf import settings
            
            # Caminho da imagem CargoSnap
            source_path = Path(settings.MEDIA_ROOT) / upload.local_image_path
            
            if not source_path.exists():
                logger.warning(f"Imagem CargoSnap não encontrada: {source_path}")
                return None
            
            # Novo caminho para inspeção
            timestamp = upload.scan_date_time.strftime('%Y/%m/%d')
            filename = f"cargosnap_{upload.cargosnap_id}_{source_path.suffix}"
            dest_relative = f"inspections/photos/{timestamp}/{filename}"
            dest_path = Path(settings.MEDIA_ROOT) / dest_relative
            
            # Criar diretório se não existir
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copiar arquivo
            shutil.copy2(source_path, dest_path)
            
            return dest_relative
            
        except Exception as e:
            logger.error(f"Erro ao copiar imagem: {str(e)}")
            return None
    
    def _parse_coordinate(self, coord_str):
        """Converte string de coordenada para Decimal"""
        if not coord_str:
            return None
        try:
            return float(coord_str)
        except (ValueError, TypeError):
            return None
    
    @transaction.atomic
    def link_existing_inspection_to_cargosnap(
        self,
        inspection: Inspection,
        container_number: str
    ) -> bool:
        """
        Vincula uma inspeção existente a um arquivo CargoSnap pelo número do container
        
        Args:
            inspection: Inspeção a ser vinculada
            container_number: Número do container
            
        Returns:
            True se vinculado com sucesso, False caso contrário
        """
        try:
            cargosnap_file = CargoSnapFile.objects.filter(
                scan_code=container_number
            ).first()
            
            if not cargosnap_file:
                logger.warning(f"Arquivo CargoSnap não encontrado para container: {container_number}")
                return False
            
            inspection.cargosnap_file = cargosnap_file
            inspection.save()
            
            logger.info(f"Inspeção {inspection.reference_number} vinculada ao CargoSnap {cargosnap_file.scan_code}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao vincular inspeção: {str(e)}")
            return False
    
    def auto_link_by_container_number(self) -> dict:
        """
        Vincula automaticamente inspeções existentes com arquivos CargoSnap
        baseado no número do container
        
        Returns:
            Dict com estatísticas do processo
        """
        stats = {
            'processed': 0,
            'linked': 0,
            'already_linked': 0,
            'not_found': 0
        }
        
        # Buscar inspeções sem vínculo CargoSnap mas com container_number
        inspections = Inspection.objects.filter(
            cargosnap_file__isnull=True,
            container_number__isnull=False
        ).exclude(container_number='')
        
        for inspection in inspections:
            stats['processed'] += 1
            
            try:
                cargosnap_file = CargoSnapFile.objects.filter(
                    scan_code=inspection.container_number
                ).first()
                
                if cargosnap_file:
                    inspection.cargosnap_file = cargosnap_file
                    inspection.save()
                    stats['linked'] += 1
                    logger.info(f"Auto-vinculado: {inspection.reference_number} -> {cargosnap_file.scan_code}")
                else:
                    stats['not_found'] += 1
                    
            except Exception as e:
                logger.error(f"Erro ao processar inspeção {inspection.id}: {str(e)}")
                continue
        
        logger.info(f"Auto-vinculação completa: {stats}")
        return stats
    
    def get_container_unified_data(self, container_number: str) -> dict:
        """
        Retorna dados unificados de container (CargoSnap + Inspeções)
        
        Args:
            container_number: Número do container
            
        Returns:
            Dict com dados unificados
        """
        # Buscar dados CargoSnap
        cargosnap_file = CargoSnapFile.objects.filter(
            scan_code=container_number
        ).prefetch_related('uploads').first()
        
        # Buscar inspeções ICTSI
        inspections = Inspection.objects.filter(
            container_number=container_number
        ).prefetch_related('photos').order_by('-created_at')
        
        return {
            'container_number': container_number,
            'cargosnap': {
                'exists': cargosnap_file is not None,
                'id': cargosnap_file.id if cargosnap_file else None,
                'total_photos': cargosnap_file.snap_count if cargosnap_file else 0,
                'damages': cargosnap_file.snap_count_with_damage if cargosnap_file else 0,
                'last_updated': cargosnap_file.updated_at if cargosnap_file else None,
                'sync_status': cargosnap_file.sync_status if cargosnap_file else None
            },
            'inspections': {
                'count': inspections.count(),
                'items': list(inspections.values(
                    'id', 'reference_number', 'status', 
                    'created_at', 'completed_at'
                ))
            },
            'total_photos': (
                (cargosnap_file.snap_count if cargosnap_file else 0) +
                sum(i.photos.count() for i in inspections)
            )
        }
