# Script para gerar e aplicar migrações da integração CargoSnap
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  MIGRAÇÕES - INTEGRAÇÃO CARGOSNAP ↔ INSPEÇÕES" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

# Ativar ambiente virtual
Write-Host "► Ativando ambiente virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Gerar migrações para inspections
Write-Host "► Gerando migrações para inspections..." -ForegroundColor Yellow
python manage.py makemigrations inspections

# Gerar migrações para cargosnap_integration (se necessário)
Write-Host "► Gerando migrações para cargosnap_integration..." -ForegroundColor Yellow
python manage.py makemigrations cargosnap_integration

# Aplicar migrações
Write-Host "► Aplicando migrações..." -ForegroundColor Yellow
python manage.py migrate

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Green
Write-Host "  ✓ MIGRAÇÕES CONCLUÍDAS COM SUCESSO!" -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Novos campos adicionados:" -ForegroundColor Cyan
Write-Host "  - Inspection.cargosnap_file" -ForegroundColor White
Write-Host "  - Inspection.imported_from_cargosnap" -ForegroundColor White
Write-Host "  - InspectionPhoto.photo_source" -ForegroundColor White
Write-Host "  - InspectionPhoto.cargosnap_upload" -ForegroundColor White
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Cyan
Write-Host "  1. Testar criação de inspeção via CargoSnap" -ForegroundColor White
Write-Host "  2. Testar upload de fotos via mobile" -ForegroundColor White
Write-Host "  3. Executar auto-vinculação: POST /api/cargosnap/files/auto_link_inspections/" -ForegroundColor White
Write-Host ""
