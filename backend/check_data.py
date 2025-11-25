import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cargosnap_integration.models import CargoSnapFile, CargoSnapUpload

total_files = CargoSnapFile.objects.count()
total_uploads = CargoSnapUpload.objects.count()
images_downloaded = CargoSnapUpload.objects.filter(image_downloaded=True).count()

print(f"Total de arquivos: {total_files}")
print(f"Total de uploads: {total_uploads}")
print(f"Imagens baixadas: {images_downloaded}")

if total_files > 0:
    print(f"\nPrimeiros 5 arquivos:")
    for file in CargoSnapFile.objects.all()[:5]:
        print(f"  - {file.scan_code} (ID: {file.id}, Uploads: {file.uploads.count()})")
