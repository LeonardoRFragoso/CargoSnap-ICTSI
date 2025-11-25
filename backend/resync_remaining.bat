@echo off
echo.
echo ============================================================
echo   RE-SINCRONIZANDO ARQUIVOS RESTANTES
echo ============================================================
echo.

python manage.py sync_cargosnap --file-id 3428297
python manage.py sync_cargosnap --file-id 3425353
python manage.py sync_cargosnap --file-id 3425331
python manage.py sync_cargosnap --file-id 3424077
python manage.py sync_cargosnap --file-id 3423400
python manage.py sync_cargosnap --file-id 3423258
python manage.py sync_cargosnap --file-id 3423021
python manage.py sync_cargosnap --file-id 3422818
python manage.py sync_cargosnap --file-id 3394877
python manage.py sync_cargosnap --file-id 3394815
python manage.py sync_cargosnap --file-id 3504068

echo.
echo ============================================================
echo   COMPLETO!
echo ============================================================
echo.
