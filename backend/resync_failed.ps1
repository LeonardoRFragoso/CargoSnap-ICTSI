# Script PowerShell para re-sincronizar arquivos que falharam
# Execute: .\resync_failed.ps1

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  RE-SINCRONIZAÇÃO DE ARQUIVOS QUE FALHARAM" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

$failedIds = @(
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
    3394815   # ICTU1345677
)

Write-Host "Total de arquivos: $($failedIds.Count)`n" -ForegroundColor Yellow

$success = 0
$failed = 0

foreach ($id in $failedIds) {
    Write-Host "Processando arquivo ID: $id" -ForegroundColor White
    
    try {
        python manage.py sync_cargosnap --file-id $id 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Sucesso`n" -ForegroundColor Green
            $success++
        } else {
            Write-Host "  ✗ Falhou`n" -ForegroundColor Red
            $failed++
        }
    } catch {
        Write-Host "  ✗ Erro: $_`n" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  RESUMO" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "✓ Sucessos: $success" -ForegroundColor Green
Write-Host "✗ Falhas: $failed" -ForegroundColor Red
Write-Host "============================================================`n" -ForegroundColor Cyan
