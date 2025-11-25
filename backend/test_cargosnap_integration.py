"""
Script de teste para verificar a integração com CargoSnap
Execute: python test_cargosnap_integration.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cargosnap_integration.services import CargoSnapAPIService
from apps.cargosnap_integration.models import (
    CargoSnapFile, CargoSnapUpload, CargoSnapSyncLog
)
from django.utils import timezone

def print_section(title):
    """Imprime uma seção formatada"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def test_api_connection():
    """Testa conexão com a API do CargoSnap"""
    print_section("TESTE 1: Conexão com API CargoSnap")
    
    try:
        service = CargoSnapAPIService()
        
        print("✓ Serviço inicializado")
        print(f"  URL Base: {service.BASE_URL}")
        print(f"  Token: {service.TOKEN[:20]}...")
        
        # Testa primeira chamada
        print("\nTestando primeira chamada (lista de arquivos)...")
        result = service.get_files_list(page=1, limit=5)
        
        print(f"✓ Conexão estabelecida!")
        print(f"  Total de arquivos: {result.get('total', 0)}")
        print(f"  Páginas: {result.get('last_page', 0)}")
        print(f"  Arquivos na primeira página: {len(result.get('data', []))}")
        
        if result.get('data'):
            primeiro = result['data'][0]
            print(f"\nPrimeiro arquivo encontrado:")
            print(f"  ID: {primeiro['id']}")
            print(f"  Container: {primeiro['scan_code']}")
            print(f"  Fotos: {primeiro['snap_count']}")
            print(f"  Data: {primeiro['created_at']}")
            
            # Testa segunda chamada
            print(f"\nTestando segunda chamada (detalhes do arquivo {primeiro['id']})...")
            details = service.get_file_details(primeiro['id'])
            
            print(f"✓ Detalhes obtidos!")
            print(f"  Uploads: {len(details.get('uploads', []))}")
            print(f"  Workflows: {len(details.get('workflow_runs', []))}")
            print(f"  Localizações: {len(details.get('locations', []))}")
            
            if details.get('uploads'):
                print(f"\nPrimeira imagem:")
                img = details['uploads'][0]
                print(f"  URL: {img['image_url']}")
                print(f"  Thumbnail: {img['image_thumb']}")
                print(f"  Workflow: {img.get('workflow_step_description', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_models():
    """Testa modelos do banco de dados"""
    print_section("TESTE 2: Modelos do Banco de Dados")
    
    try:
        # Conta registros
        total_files = CargoSnapFile.objects.count()
        total_uploads = CargoSnapUpload.objects.count()
        total_logs = CargoSnapSyncLog.objects.count()
        
        print(f"✓ Modelos acessíveis")
        print(f"  Arquivos (CargoSnapFile): {total_files}")
        print(f"  Uploads (CargoSnapUpload): {total_uploads}")
        print(f"  Logs de Sync (CargoSnapSyncLog): {total_logs}")
        
        if total_files > 0:
            print("\nÚltimos 5 arquivos no banco:")
            for file in CargoSnapFile.objects.all()[:5]:
                print(f"  • {file.scan_code} - {file.snap_count} fotos - Status: {file.sync_status}")
        
        if total_logs > 0:
            print("\nÚltima sincronização:")
            last_log = CargoSnapSyncLog.objects.order_by('-started_at').first()
            print(f"  Data: {last_log.started_at}")
            print(f"  Status: {last_log.status}")
            print(f"  Arquivos processados: {last_log.files_processed}")
            print(f"  Imagens baixadas: {last_log.images_downloaded}")
        
        return True
        
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_sync_single_file():
    """Testa sincronização de um único arquivo"""
    print_section("TESTE 3: Sincronização de Arquivo Individual")
    
    try:
        service = CargoSnapAPIService()
        
        # Busca primeiro arquivo da API
        print("Buscando primeiro arquivo da API...")
        result = service.get_files_list(page=1, limit=1)
        
        if not result.get('data'):
            print("✗ Nenhum arquivo encontrado na API")
            return False
        
        file_data = result['data'][0]
        file_id = file_data['id']
        
        print(f"✓ Arquivo encontrado: {file_data['scan_code']} (ID: {file_id})")
        
        # Sincroniza
        print("\nSincronizando arquivo...")
        file_obj, created = service.sync_file(file_data)
        
        action = "Criado" if created else "Atualizado"
        print(f"✓ Arquivo {action} no banco de dados")
        print(f"  ID local: {file_obj.id}")
        print(f"  Container: {file_obj.scan_code}")
        
        # Busca detalhes
        print("\nBuscando detalhes completos...")
        details = service.get_file_details(file_id)
        
        # Sincroniza detalhes
        print("Sincronizando detalhes...")
        service.sync_file_details(file_obj, details)
        
        print(f"✓ Detalhes sincronizados!")
        
        # Verifica uploads
        uploads_count = file_obj.uploads.count()
        print(f"  Uploads salvos: {uploads_count}")
        
        if uploads_count > 0:
            print("\nPrimeiras 3 imagens:")
            for upload in file_obj.uploads.all()[:3]:
                status = "✓ Baixada" if upload.image_downloaded else "○ Pendente"
                print(f"  {status} - {upload.workflow_step_description or 'Sem descrição'}")
        
        return True
        
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_image_download():
    """Testa download de imagens"""
    print_section("TESTE 4: Download de Imagens")
    
    try:
        # Busca arquivo com imagens não baixadas
        file_with_pending = CargoSnapFile.objects.filter(
            uploads__image_downloaded=False
        ).first()
        
        if not file_with_pending:
            print("⚠ Nenhum arquivo com imagens pendentes encontrado")
            print("  (Todas as imagens já foram baixadas ou não há arquivos)")
            return True
        
        print(f"Arquivo selecionado: {file_with_pending.scan_code}")
        
        pending_count = file_with_pending.uploads.filter(image_downloaded=False).count()
        print(f"Imagens pendentes: {pending_count}")
        
        if pending_count > 3:
            print(f"\n⚠ Muitas imagens pendentes ({pending_count})")
            print("  Por questões de tempo, vamos baixar apenas 2 para teste")
            
            # Baixa apenas 2 imagens para teste
            service = CargoSnapAPIService()
            for upload in file_with_pending.uploads.filter(image_downloaded=False)[:2]:
                print(f"\nBaixando: {upload.workflow_step_description or 'Imagem'}...")
                success = service._download_upload_images(upload)
                
                if success:
                    print(f"  ✓ Baixada com sucesso!")
                    print(f"    Local: {upload.local_image_path}")
                else:
                    print(f"  ✗ Falha no download")
        else:
            # Baixa todas
            service = CargoSnapAPIService()
            downloaded, failed = service.download_file_images(file_with_pending)
            
            print(f"\n✓ Download concluído!")
            print(f"  Sucesso: {downloaded}")
            print(f"  Falhas: {failed}")
        
        return True
        
    except Exception as e:
        print(f"✗ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def show_summary():
    """Mostra resumo do sistema"""
    print_section("RESUMO DO SISTEMA")
    
    try:
        # Estatísticas
        total_files = CargoSnapFile.objects.count()
        total_uploads = CargoSnapUpload.objects.count()
        downloaded = CargoSnapUpload.objects.filter(image_downloaded=True).count()
        pending = total_uploads - downloaded
        with_damage = CargoSnapFile.objects.filter(snap_count_with_damage__gt=0).count()
        
        print(f"Arquivos (Containers): {total_files}")
        print(f"Imagens totais: {total_uploads}")
        print(f"  ✓ Baixadas: {downloaded}")
        print(f"  ○ Pendentes: {pending}")
        print(f"Containers com avarias: {with_damage}")
        
        # Status de sincronização
        print("\nStatus de Sincronização:")
        for status, count in CargoSnapFile.objects.values_list('sync_status').annotate(
            count=models.Count('id')
        ):
            print(f"  {status}: {count}")
        
        # Última sincronização
        last_log = CargoSnapSyncLog.objects.order_by('-started_at').first()
        if last_log:
            print(f"\nÚltima sincronização: {last_log.started_at.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"  Status: {last_log.status}")
        
    except Exception as e:
        print(f"Erro ao gerar resumo: {str(e)}")

def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("  TESTE DE INTEGRAÇÃO CARGOSNAP")
    print("=" * 80)
    print(f"\nData/Hora: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    results = []
    
    # Executa testes
    results.append(("Conexão API", test_api_connection()))
    results.append(("Modelos DB", test_database_models()))
    results.append(("Sincronização", test_sync_single_file()))
    results.append(("Download Imagens", test_image_download()))
    
    # Resumo
    show_summary()
    
    # Resultado final
    print_section("RESULTADO DOS TESTES")
    
    for test_name, success in results:
        status = "✓ PASSOU" if success else "✗ FALHOU"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema funcionando corretamente.")
        print("\nPróximos passos:")
        print("  1. Execute: python manage.py sync_cargosnap")
        print("  2. Acesse a interface em: http://localhost:5173/cargosnap")
    else:
        print("\n⚠ ALGUNS TESTES FALHARAM. Verifique os erros acima.")

if __name__ == '__main__':
    from django.db import models
    main()
