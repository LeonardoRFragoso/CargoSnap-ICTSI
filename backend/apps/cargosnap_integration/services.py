import requests
import os
import time
from pathlib import Path
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from typing import Dict, List, Optional, Tuple
import logging

from .models import (
    CargoSnapFile, CargoSnapUpload, CargoSnapLocation,
    CargoSnapWorkflow, CargoSnapWorkflowStep, CargoSnapWorkflowRun,
    CargoSnapWorkflowRunStep, CargoSnapFormSubmit, CargoSnapField,
    CargoSnapSyncLog
)

logger = logging.getLogger(__name__)


class CargoSnapAPIService:
    """Serviço para integração com a API do CargoSnap"""
    
    BASE_URL = "https://api.cargosnap.com/api/v2"
    TOKEN = "eW15Y1FGeXRqOEZRa3AxRlFRcXRMaGJyVmxMQjRVM3FfMTMwNQ=="
    
    def __init__(self):
        self.session = requests.Session()
        self.session.params = {'token': self.TOKEN}
        
        # Diretório para salvar imagens
        self.media_root = getattr(settings, 'MEDIA_ROOT', 'media')
        self.images_dir = Path(self.media_root) / 'cargosnap' / 'images'
        self.thumbs_dir = Path(self.media_root) / 'cargosnap' / 'thumbs'
        
        # Criar diretórios se não existirem
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.thumbs_dir.mkdir(parents=True, exist_ok=True)
    
    def get_files_list(self, page: int = 1, limit: int = 10) -> Dict:
        """Busca lista de arquivos com paginação"""
        url = f"{self.BASE_URL}/files"
        params = {'page': page, 'limit': limit}
        
        try:
            # Timeout aumentado para 90 segundos
            response = self.session.get(url, params=params, timeout=90)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar lista de arquivos (página {page}): {str(e)}")
            raise
    
    def get_file_details(self, file_id: int) -> Dict:
        """Busca detalhes completos de um arquivo específico"""
        url = f"{self.BASE_URL}/files/{file_id}"
        
        try:
            # Timeout aumentado para 90 segundos
            response = self.session.get(url, timeout=90)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar detalhes do arquivo {file_id}: {str(e)}")
            raise
    
    def download_image(self, url: str, save_path: Path, max_retries: int = 3) -> bool:
        """Faz download de uma imagem com retry logic"""
        for attempt in range(max_retries):
            try:
                # Timeout aumentado para 180 segundos (3 minutos)
                response = requests.get(url, timeout=180, stream=True)
                response.raise_for_status()
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Sucesso!
                if attempt > 0:
                    logger.info(f"Imagem baixada com sucesso na tentativa {attempt + 1}: {url}")
                return True
                
            except requests.exceptions.Timeout as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5  # 5, 10, 15 segundos
                    logger.warning(f"Timeout ao baixar {url}. Tentativa {attempt + 1}/{max_retries}. Aguardando {wait_time}s...")
                    print(f"           ⚠ Timeout - tentando novamente em {wait_time}s... (tentativa {attempt + 2}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Timeout final ao baixar imagem após {max_retries} tentativas: {url}")
                    print(f"           ✗ Timeout final após {max_retries} tentativas")
                    return False
                    
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 504:  # Gateway Timeout
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5
                        logger.warning(f"Gateway timeout (504) ao baixar {url}. Tentativa {attempt + 1}/{max_retries}. Aguardando {wait_time}s...")
                        print(f"           ⚠ Gateway timeout (504) - tentando novamente em {wait_time}s... (tentativa {attempt + 2}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Gateway timeout final (504) após {max_retries} tentativas: {url}")
                        print(f"           ✗ Gateway timeout (504) final após {max_retries} tentativas")
                        return False
                else:
                    logger.error(f"Erro HTTP {e.response.status_code} ao baixar imagem {url}: {str(e)}")
                    print(f"           ✗ Erro HTTP {e.response.status_code}")
                    return False
                    
            except Exception as e:
                logger.error(f"Erro ao baixar imagem {url}: {str(e)}")
                return False
        
        return False
    
    @transaction.atomic
    def sync_file(self, file_data: Dict) -> Tuple[CargoSnapFile, bool]:
        """Sincroniza um arquivo do CargoSnap"""
        
        file_id = file_data['id']
        
        # Verifica se o arquivo já existe
        try:
            file_obj = CargoSnapFile.objects.get(cargosnap_id=file_id)
            created = False
        except CargoSnapFile.DoesNotExist:
            file_obj = CargoSnapFile(cargosnap_id=file_id)
            created = True
        
        # Atualiza campos
        file_obj.scan_code = file_data.get('scan_code', '')
        file_obj.scan_code_format = file_data.get('scan_code_format', '')
        file_obj.closed = bool(file_data.get('closed', 0))
        file_obj.created_at = self._parse_datetime(file_data.get('created_at'))
        file_obj.updated_at = self._parse_datetime(file_data.get('updated_at'))
        file_obj.recent_snap_id = file_data.get('recent_snap_id')
        file_obj.snap_count = file_data.get('snap_count', 0)
        file_obj.snap_count_with_damage = file_data.get('snap_count_with_damage', 0)
        file_obj.sync_status = 'pending'
        
        file_obj.save()
        
        return file_obj, created
    
    @transaction.atomic
    def sync_file_details(self, file_obj: CargoSnapFile, details: Dict) -> None:
        """Sincroniza todos os detalhes de um arquivo"""
        
        try:
            file_obj.sync_status = 'syncing'
            file_obj.save()
            
            # Sincroniza uploads (fotos)
            for upload_data in details.get('uploads', []):
                self._sync_upload(file_obj, upload_data)
            
            # Sincroniza locations
            for location_data in details.get('locations', []):
                self._sync_location(file_obj, location_data)
            
            # Sincroniza fields
            for field_data in details.get('fields', []):
                self._sync_field(file_obj, field_data)
            
            # Sincroniza form_submits
            for form_data in details.get('form_submits', []):
                self._sync_form_submit(file_obj, form_data)
            
            # Sincroniza workflow_runs
            for workflow_run_data in details.get('workflow_runs', []):
                self._sync_workflow_run(file_obj, workflow_run_data)
            
            file_obj.sync_status = 'completed'
            file_obj.sync_error = None
            file_obj.save()
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar detalhes do arquivo {file_obj.cargosnap_id}: {str(e)}")
            file_obj.sync_status = 'error'
            file_obj.sync_error = str(e)
            file_obj.save()
            raise
    
    def _sync_upload(self, file_obj: CargoSnapFile, upload_data: Dict) -> CargoSnapUpload:
        """Sincroniza um upload (foto)"""
        
        upload_id = upload_data['id']
        
        upload_obj, created = CargoSnapUpload.objects.update_or_create(
            cargosnap_id=upload_id,
            defaults={
                'file': file_obj,
                'tenant_id': upload_data.get('tenant_id'),
                'device_id': upload_data.get('device_id'),
                'device_nick': upload_data.get('device_nick', ''),
                'upload_type': upload_data.get('upload_type', ''),
                'created_at': self._parse_datetime(upload_data.get('created_at')),
                'scan_date_time': self._parse_datetime(upload_data.get('scan_date_time')),
                'longitude': upload_data.get('longitude', ''),
                'latitude': upload_data.get('latitude', ''),
                'geocoding_data': upload_data.get('geocoding'),
                'has_damage': bool(upload_data.get('has_damage', 0)),
                'damage_type_id': upload_data.get('damage_type_id'),
                'damage_type_desc': upload_data.get('damage_type_desc', ''),
                'comment': upload_data.get('comment', ''),
                'document_type_id': upload_data.get('document_type_id'),
                'document_type_desc': upload_data.get('document_type_desc', ''),
                'workflow_id': upload_data.get('workflow_id'),
                'workflow_step_id': upload_data.get('workflow_step_id'),
                'workflow_description': upload_data.get('workflow_description', ''),
                'workflow_step_description': upload_data.get('workflow_step_description', ''),
                'image_path': upload_data.get('image_path', ''),
                'image_url': upload_data.get('image_url', ''),
                'image_thumb': upload_data.get('image_thumb', ''),
            }
        )
        
        return upload_obj
    
    def _sync_location(self, file_obj: CargoSnapFile, location_data: Dict) -> CargoSnapLocation:
        """Sincroniza uma localização"""
        
        location_obj, created = CargoSnapLocation.objects.update_or_create(
            file=file_obj,
            cargosnap_id=location_data.get('id'),
            defaults={
                'location': location_data.get('location', '')
            }
        )
        
        return location_obj
    
    def _sync_field(self, file_obj: CargoSnapFile, field_data: Dict) -> CargoSnapField:
        """Sincroniza um campo customizado"""
        
        # Assumindo que field_data tem algum identificador único
        # Adapte conforme a estrutura real dos dados
        field_obj = CargoSnapField.objects.create(
            file=file_obj,
            field_name=field_data.get('name', ''),
            field_value=field_data.get('value', ''),
            field_data=field_data
        )
        
        return field_obj
    
    def _sync_form_submit(self, file_obj: CargoSnapFile, form_data: Dict) -> CargoSnapFormSubmit:
        """Sincroniza um formulário submetido"""
        
        form_id = form_data.get('id')
        
        form_obj, created = CargoSnapFormSubmit.objects.update_or_create(
            cargosnap_id=form_id,
            defaults={
                'file': file_obj,
                'form_data': form_data
            }
        )
        
        return form_obj
    
    def _sync_workflow_run(self, file_obj: CargoSnapFile, workflow_run_data: Dict) -> CargoSnapWorkflowRun:
        """Sincroniza uma execução de workflow"""
        
        # Primeiro sincroniza o workflow
        workflow_data = workflow_run_data.get('workflow', {})
        if workflow_data:
            workflow_obj = self._sync_workflow(workflow_data)
        else:
            workflow_obj = None
        
        run_id = workflow_run_data['id']
        
        run_obj, created = CargoSnapWorkflowRun.objects.update_or_create(
            cargosnap_id=run_id,
            defaults={
                'file': file_obj,
                'workflow': workflow_obj,
                'client_key': workflow_run_data.get('client_key', ''),
                'tenant_id': workflow_run_data.get('tenant_id'),
                'submit_date_time': self._parse_datetime(workflow_run_data.get('submit_date_time')),
                'created_at': self._parse_datetime(workflow_run_data.get('created_at')),
                'updated_at': self._parse_datetime(workflow_run_data.get('updated_at')),
                'deleted_at': self._parse_datetime(workflow_run_data.get('deleted_at')),
                'completed_at': self._parse_datetime(workflow_run_data.get('completed_at')),
                'started_on_device_at': self._parse_datetime(workflow_run_data.get('started_on_device_at')),
                'finished_on_device_at': self._parse_datetime(workflow_run_data.get('finished_on_device_at')),
            }
        )
        
        # Sincroniza workflow run steps
        for step_data in workflow_run_data.get('workflow_run_steps', []):
            self._sync_workflow_run_step(run_obj, step_data)
        
        return run_obj
    
    def _sync_workflow(self, workflow_data: Dict) -> CargoSnapWorkflow:
        """Sincroniza um workflow"""
        
        workflow_id = workflow_data['id']
        
        workflow_obj, created = CargoSnapWorkflow.objects.update_or_create(
            cargosnap_id=workflow_id,
            defaults={
                'tenant_id': workflow_data.get('tenant_id'),
                'name': workflow_data.get('name', ''),
                'workflow_type': workflow_data.get('type', ''),
                'force': bool(workflow_data.get('force', False)),
                'created_at': self._parse_datetime(workflow_data.get('created_at')),
                'updated_at': self._parse_datetime(workflow_data.get('updated_at')),
                'deleted_at': self._parse_datetime(workflow_data.get('deleted_at')),
                'language': workflow_data.get('language', ''),
                'location_filter': workflow_data.get('location_filter', ''),
                'close_file_after_completion': bool(workflow_data.get('close_file_after_completion', False)),
                'order': workflow_data.get('order', 0),
                'clear_app_after_completion': bool(workflow_data.get('clear_app_after_completion', False)),
                'info_url': workflow_data.get('info_url', ''),
            }
        )
        
        # Sincroniza workflow steps
        for step_data in workflow_data.get('steps', []):
            self._sync_workflow_step(workflow_obj, step_data)
        
        return workflow_obj
    
    def _sync_workflow_step(self, workflow_obj: CargoSnapWorkflow, step_data: Dict) -> CargoSnapWorkflowStep:
        """Sincroniza uma etapa de workflow"""
        
        step_id = step_data['id']
        
        step_obj, created = CargoSnapWorkflowStep.objects.update_or_create(
            cargosnap_id=step_id,
            defaults={
                'workflow': workflow_obj,
                'tenant_id': step_data.get('tenant_id'),
                'order': step_data.get('order', 0),
                'description': step_data.get('description', ''),
                'step_type': step_data.get('type', ''),
                'allow_skip': bool(step_data.get('allow_skip', False)),
                'platform_description': step_data.get('platform_description', ''),
                'data': step_data.get('data'),
                'deleted_at': self._parse_datetime(step_data.get('deleted_at')),
                'info_url': step_data.get('info_url', ''),
            }
        )
        
        return step_obj
    
    def _sync_workflow_run_step(self, run_obj: CargoSnapWorkflowRun, step_data: Dict) -> Optional[CargoSnapWorkflowRunStep]:
        """Sincroniza uma etapa executada de workflow"""
        
        step_id = step_data['id']
        workflow_step_id = step_data.get('workflow_step_id')
        
        # Busca o workflow step
        try:
            workflow_step = CargoSnapWorkflowStep.objects.get(cargosnap_id=workflow_step_id)
        except CargoSnapWorkflowStep.DoesNotExist:
            logger.warning(f"Workflow step {workflow_step_id} não encontrado - pulando run step {step_id}")
            # Se o workflow step não existe, não podemos criar o run step
            # pois workflow_step é um campo obrigatório
            return None
        
        run_step_obj, created = CargoSnapWorkflowRunStep.objects.update_or_create(
            cargosnap_id=step_id,
            defaults={
                'workflow_run': run_obj,
                'workflow_step': workflow_step,
                'entity_type': step_data.get('entity_type', ''),
                'status': step_data.get('status', ''),
                'entity_ids': step_data.get('entity_ids', []),
                'device_id': step_data.get('device_id'),
                'tenant_id': step_data.get('tenant_id'),
                'submit_date_time': self._parse_datetime(step_data.get('submit_date_time')),
                'created_at': self._parse_datetime(step_data.get('created_at')),
                'updated_at': self._parse_datetime(step_data.get('updated_at')),
                'deleted_at': self._parse_datetime(step_data.get('deleted_at')),
            }
        )
        
        return run_step_obj
    
    def download_file_images(self, file_obj: CargoSnapFile, force_download: bool = False) -> Tuple[int, int]:
        """Baixa todas as imagens de um arquivo"""
        
        downloaded = 0
        failed = 0
        
        # Se force_download, pega todas as imagens; senão, apenas as não baixadas
        if force_download:
            uploads_query = file_obj.uploads.all()
        else:
            uploads_query = file_obj.uploads.filter(image_downloaded=False)
        
        for upload in uploads_query:
            success = self._download_upload_images(upload, force_download=force_download)
            if success:
                downloaded += 1
            else:
                failed += 1
        
        return downloaded, failed
    
    def _download_upload_images(self, upload: CargoSnapUpload, force_download: bool = False) -> bool:
        """Baixa as imagens de um upload"""
        
        try:
            # Se não for force_download e já está baixado, pula
            if upload.image_downloaded and not force_download:
                return True
            # Nome do arquivo baseado no ID e timestamp
            timestamp = upload.scan_date_time.strftime('%Y%m%d_%H%M%S')
            base_filename = f"{upload.file.scan_code}_{upload.cargosnap_id}_{timestamp}"
            
            # Download da imagem completa
            if upload.image_url:
                image_ext = Path(upload.image_url).suffix or '.jpg'
                image_filename = f"{base_filename}{image_ext}"
                image_path = self.images_dir / image_filename
                
                if self.download_image(upload.image_url, image_path):
                    upload.local_image_path = str(image_path.relative_to(self.media_root))
                else:
                    return False
            
            # Download da thumbnail
            if upload.image_thumb:
                thumb_ext = Path(upload.image_thumb).suffix or '.jpg'
                thumb_filename = f"{base_filename}_thumb{thumb_ext}"
                thumb_path = self.thumbs_dir / thumb_filename
                
                if self.download_image(upload.image_thumb, thumb_path):
                    upload.local_thumb_path = str(thumb_path.relative_to(self.media_root))
                else:
                    return False
            
            upload.image_downloaded = True
            upload.save()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao baixar imagens do upload {upload.cargosnap_id}: {str(e)}")
            return False
    
    def _parse_datetime(self, datetime_str: Optional[str]) -> Optional[datetime]:
        """Converte string de data/hora para datetime"""
        if not datetime_str:
            return None
        
        try:
            # Tenta parsing com timezone
            if datetime_str.endswith('Z'):
                datetime_str = datetime_str[:-1] + '+00:00'
            
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            
            # Garante que tem timezone
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            
            return dt
        except Exception as e:
            logger.error(f"Erro ao fazer parse de datetime '{datetime_str}': {str(e)}")
            return None
    
    def full_sync(self, download_images: bool = True, force_download: bool = False, limit: int = 10) -> CargoSnapSyncLog:
        """Executa sincronização completa"""
        
        sync_log = CargoSnapSyncLog.objects.create(status='running')
        
        try:
            # Busca primeira página para descobrir total de páginas
            first_page = self.get_files_list(page=1, limit=limit)
            total_pages = first_page.get('last_page', 1)
            sync_log.total_pages = total_pages
            sync_log.save()
            
            logger.info(f"Iniciando sincronização de {total_pages} página(s)")
            print(f"\n📦 Total de páginas a processar: {total_pages}")
            
            # Processa todas as páginas
            for page in range(1, total_pages + 1):
                sync_log.current_page = page
                sync_log.save()
                
                logger.info(f"Processando página {page}/{total_pages}")
                print(f"\n📄 Processando página {page}/{total_pages}...")
                
                if page == 1:
                    page_data = first_page
                else:
                    page_data = self.get_files_list(page=page, limit=limit)
                
                files_in_page = page_data.get('data', [])
                print(f"   └─ {len(files_in_page)} arquivos nesta página")
                
                # Processa cada arquivo da página
                for idx, file_data in enumerate(files_in_page, 1):
                    try:
                        sync_log.files_processed += 1
                        container_code = file_data.get('scan_code', 'N/A')
                        
                        print(f"\n   [{idx}/{len(files_in_page)}] Container: {container_code}")
                        
                        # Sincroniza dados básicos do arquivo
                        file_obj, created = self.sync_file(file_data)
                        action = "✓ Criado" if created else "✓ Atualizado"
                        print(f"        {action}")
                        
                        if created:
                            sync_log.files_created += 1
                        else:
                            sync_log.files_updated += 1
                        
                        # Busca e sincroniza detalhes completos
                        details = self.get_file_details(file_data['id'])
                        self.sync_file_details(file_obj, details)
                        print(f"        ✓ Detalhes sincronizados")
                        
                        # Download de imagens se solicitado
                        if download_images:
                            total_uploads = file_obj.uploads.count()
                            print(f"        📥 Baixando {total_uploads} imagens...")
                            downloaded, failed = self.download_file_images(file_obj, force_download=force_download)
                            sync_log.images_downloaded += downloaded
                            sync_log.images_failed += failed
                            print(f"        ✓ Baixadas: {downloaded} | ✗ Falhas: {failed}")
                        
                        sync_log.save()
                        
                    except Exception as e:
                        logger.error(f"Erro ao processar arquivo {file_data.get('id')}: {str(e)}")
                        print(f"        ✗ ERRO: {str(e)}")
                        sync_log.files_failed += 1
                        sync_log.save()
            
            sync_log.status = 'completed'
            sync_log.finished_at = timezone.now()
            sync_log.save()
            
            logger.info(f"Sincronização completa! Arquivos: {sync_log.files_processed}, "
                       f"Criados: {sync_log.files_created}, Atualizados: {sync_log.files_updated}, "
                       f"Imagens: {sync_log.images_downloaded}")
            
            # Resumo final
            print(f"\n{'='*60}")
            print(f"🎉 SINCRONIZAÇÃO COMPLETA!")
            print(f"{'='*60}")
            print(f"📦 Arquivos processados: {sync_log.files_processed}")
            print(f"   ├─ ✓ Criados: {sync_log.files_created}")
            print(f"   ├─ ✓ Atualizados: {sync_log.files_updated}")
            print(f"   └─ ✗ Falhas: {sync_log.files_failed}")
            if download_images:
                print(f"\n📷 Imagens:")
                print(f"   ├─ ✓ Baixadas: {sync_log.images_downloaded}")
                print(f"   └─ ✗ Falhas: {sync_log.images_failed}")
            print(f"\n⏱️  Tempo: {(sync_log.finished_at - sync_log.started_at).total_seconds():.1f}s")
            print(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Erro na sincronização: {str(e)}")
            print(f"\n{'='*60}")
            print(f"❌ ERRO NA SINCRONIZAÇÃO")
            print(f"{'='*60}")
            print(f"Erro: {str(e)}")
            print(f"{'='*60}\n")
            sync_log.status = 'error'
            sync_log.error_message = str(e)
            sync_log.finished_at = timezone.now()
            sync_log.save()
            raise
        
        return sync_log
