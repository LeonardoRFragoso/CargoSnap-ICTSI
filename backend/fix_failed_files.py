"""
Script para re-sincronizar arquivos que falharam
Execute: python manage.py shell < fix_failed_files.py
"""

import django
import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cargosnap_integration.services import CargoSnapAPIService
from apps.cargosnap_integration.models import CargoSnapFile

# IDs dos arquivos que falharam
failed_file_ids = [
    3504068,  # HASU1234566 - Connection reset
    3438635,  # SZLU9140670
    3431558,  # JOLU1188002
    3431319,  # CXDU1809346
    3428297,  # NINU1234567
    3425353,  # CAIU3620840
    3425331,  # GLDU3916030
    3424077,  # UACU4145611
    3423400,  # MWMU6375015
    3423258,  # TEMU3186419
    3423021,  # PCIU9035883
    3422818,  # SUDU1324560
    3394877,  # SUDU1234567
    3394815,  # ICTU1345677
]

print("\n" + "="*70)
print("  RE-SINCRONIZAÇÃO DE ARQUIVOS QUE FALHARAM")
print("="*70)
print(f"\nTotal de arquivos a processar: {len(failed_file_ids)}\n")

service = CargoSnapAPIService()
success_count = 0
failed_count = 0
failed_list = []

for idx, file_id in enumerate(failed_file_ids, 1):
    print(f"\n[{idx}/{len(failed_file_ids)}] Processando arquivo ID {file_id}...")
    
    try:
        # Busca detalhes do arquivo
        details = service.get_file_details(file_id)
        scan_code = details.get('scan_code', 'N/A')
        
        print(f"   Container: {scan_code}")
        
        # Sincroniza dados básicos
        file_obj, created = service.sync_file(details)
        action = "Criado" if created else "Atualizado"
        print(f"   ✓ {action}")
        
        # Sincroniza detalhes (incluindo workflows)
        service.sync_file_details(file_obj, details)
        print(f"   ✓ Detalhes sincronizados")
        
        # Download de imagens se necessário
        uploads_pending = file_obj.uploads.filter(image_downloaded=False).count()
        if uploads_pending > 0:
            print(f"   📥 Baixando {uploads_pending} imagens pendentes...")
            downloaded, failed = service.download_file_images(file_obj)
            print(f"   ✓ Baixadas: {downloaded} | ✗ Falhas: {failed}")
        else:
            print(f"   ✓ Todas as imagens já baixadas")
        
        success_count += 1
        print(f"   ✅ SUCESSO")
        
    except Exception as e:
        print(f"   ❌ ERRO: {str(e)}")
        failed_count += 1
        failed_list.append((file_id, str(e)))

# Resumo
print(f"\n{'='*70}")
print("  RESUMO")
print(f"{'='*70}")
print(f"\n✅ Sucessos: {success_count}")
print(f"❌ Falhas: {failed_count}")

if failed_list:
    print(f"\n📋 Arquivos que ainda falharam:")
    for file_id, error in failed_list:
        print(f"   - ID {file_id}: {error[:80]}...")

print(f"\n{'='*70}\n")
