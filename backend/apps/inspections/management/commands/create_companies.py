"""
Management command to create default companies
Usage: python manage.py create_companies
"""
from django.core.management.base import BaseCommand
from apps.core.models import Company


class Command(BaseCommand):
    help = 'Cria as 3 empresas padrão do sistema'

    def handle(self, *args, **options):
        companies = [
            {
                'name': 'ICTSI',
                'slug': 'ictsi',
                'company_type': 'ICTSI',
                'email': 'contact@ictsi.com',
                'phone': '+1-555-0100',
                'website': 'https://www.ictsi.com',
                'address': '1000 Corporate Drive',
                'city': 'Manila',
                'state': 'MN',
                'zip_code': '1000',
                'country': 'Philippines',
                'primary_color': '#0066CC',
                'secondary_color': '#003366',
            },
            {
                'name': 'iTracker',
                'slug': 'itracker',
                'company_type': 'ITRACKER',
                'email': 'info@itracker.com.br',
                'phone': '+55-71-3000-0000',
                'website': 'https://www.itracker.com.br',
                'address': 'Avenida Principal, 100',
                'city': 'Salvador',
                'state': 'BA',
                'zip_code': '40000-000',
                'country': 'Brasil',
                'primary_color': '#FF6600',
                'secondary_color': '#CC5200',
            },
            {
                'name': 'CLIA',
                'slug': 'clia',
                'company_type': 'CLIA',
                'email': 'contato@clia.com.br',
                'phone': '+55-71-3200-0000',
                'website': 'https://www.clia.com.br',
                'address': 'Rodovia BA-522, KM 20',
                'city': 'Simões Filho',
                'state': 'BA',
                'zip_code': '43700-000',
                'country': 'Brasil',
                'primary_color': '#009933',
                'secondary_color': '#006622',
            },
        ]

        created_count = 0
        for company_data in companies:
            company, created = Company.objects.get_or_create(
                slug=company_data['slug'],
                defaults=company_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Empresa criada: {company.name}'))
                created_count += 1
            else:
                self.stdout.write(f'  Empresa já existe: {company.name}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'✅ Processo concluído!'))
        self.stdout.write(f'Total de empresas criadas: {created_count}/3')
