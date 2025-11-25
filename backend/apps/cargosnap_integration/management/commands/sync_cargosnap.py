from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.cargosnap_integration.services import CargoSnapAPIService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sincroniza dados do CargoSnap API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-images',
            action='store_true',
            help='Não baixar imagens, apenas sincronizar dados'
        )
        parser.add_argument(
            '--force-download',
            action='store_true',
            help='Forçar re-download de todas as imagens, mesmo as já baixadas'
        )
        parser.add_argument(
            '--file-id',
            type=int,
            help='Sincronizar apenas um arquivo específico'
        )
        parser.add_argument(
            '--page',
            type=int,
            help='Sincronizar apenas uma página específica'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Número de arquivos por página (padrão: 10)'
        )

    def handle(self, *args, **options):
        download_images = not options.get('no_images', False)
        force_download = options.get('force_download', False)
        file_id = options.get('file_id')
        page = options.get('page')
        limit = options.get('limit', 10)
        
        self.stdout.write(self.style.SUCCESS('Iniciando sincronização do CargoSnap...'))
        self.stdout.write(f'Configuração: {limit} arquivos por página')
        
        if force_download:
            self.stdout.write(self.style.WARNING('⚠️  Modo FORCE DOWNLOAD ativado - todas as imagens serão baixadas novamente'))
        
        service = CargoSnapAPIService()
        
        try:
            if file_id:
                # Sincroniza apenas um arquivo específico
                self.stdout.write(f'Sincronizando arquivo {file_id}...')
                
                details = service.get_file_details(file_id)
                file_obj, created = service.sync_file(details)
                service.sync_file_details(file_obj, details)
                
                if download_images:
                    self.stdout.write('Baixando imagens...')
                    downloaded, failed = service.download_file_images(file_obj, force_download=force_download)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Imagens: {downloaded} baixadas, {failed} falharam'
                        )
                    )
                
                action = 'Criado' if created else 'Atualizado'
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{action} arquivo: {file_obj.scan_code}'
                    )
                )
            
            elif page:
                # Sincroniza apenas uma página específica
                self.stdout.write(f'Sincronizando página {page}...')
                
                page_data = service.get_files_list(page=page, limit=limit)
                total = len(page_data.get('data', []))
                
                for idx, file_data in enumerate(page_data.get('data', []), 1):
                    self.stdout.write(f'Processando arquivo {idx}/{total}: {file_data["scan_code"]}')
                    
                    file_obj, created = service.sync_file(file_data)
                    details = service.get_file_details(file_data['id'])
                    service.sync_file_details(file_obj, details)
                    
                    if download_images:
                        downloaded, failed = service.download_file_images(file_obj, force_download=force_download)
                        self.stdout.write(f'  Imagens: {downloaded} baixadas, {failed} falharam')
                
                self.stdout.write(
                    self.style.SUCCESS(f'Página {page} sincronizada com sucesso!')
                )
            
            else:
                # Sincronização completa
                self.stdout.write('Executando sincronização completa...')
                
                sync_log = service.full_sync(download_images=download_images, force_download=force_download, limit=limit)
                
                self.stdout.write(self.style.SUCCESS('Sincronização concluída!'))
                self.stdout.write(f'Status: {sync_log.status}')
                self.stdout.write(f'Arquivos processados: {sync_log.files_processed}')
                self.stdout.write(f'Arquivos criados: {sync_log.files_created}')
                self.stdout.write(f'Arquivos atualizados: {sync_log.files_updated}')
                self.stdout.write(f'Arquivos com erro: {sync_log.files_failed}')
                
                if download_images:
                    self.stdout.write(f'Imagens baixadas: {sync_log.images_downloaded}')
                    self.stdout.write(f'Imagens com erro: {sync_log.images_failed}')
                
                if sync_log.error_message:
                    self.stdout.write(
                        self.style.ERROR(f'Erro: {sync_log.error_message}')
                    )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro na sincronização: {str(e)}')
            )
            logger.exception('Erro na sincronização do CargoSnap')
            raise
