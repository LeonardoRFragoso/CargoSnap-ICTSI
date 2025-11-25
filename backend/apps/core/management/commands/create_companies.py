"""
Management command to create initial companies
Usage: python manage.py create_companies
"""
from django.core.management.base import BaseCommand
from apps.core.models import Company


class Command(BaseCommand):
    help = 'Cria as empresas iniciais do sistema (ICTSI, iTracker, CLIA)'
    
    def handle(self, *args, **options):
        companies_data = [
            {
                'name': 'ICTSI',
                'slug': 'ictsi',
                'company_type': 'ICTSI',
                'email': 'contato@ictsi.com.br',
                'phone': '+55 71 3366-5800',
                'website': 'https://www.ictsi.com.br',
                'address': 'Terminal de Contêineres de Salvador',
                'city': 'Salvador',
                'state': 'BA',
                'zip_code': '40000-000',
                'country': 'Brasil',
                'primary_color': '#003366',
                'secondary_color': '#0066CC',
            },
            {
                'name': 'iTracker',
                'slug': 'itracker',
                'company_type': 'ITRACKER',
                'email': 'contato@itracker.com.br',
                'phone': '+55 71 3366-5900',
                'website': 'https://www.itracker.com.br',
                'address': 'Centro Empresarial',
                'city': 'Salvador',
                'state': 'BA',
                'zip_code': '40000-000',
                'country': 'Brasil',
                'primary_color': '#FF6600',
                'secondary_color': '#FF9933',
            },
            {
                'name': 'CLIA',
                'slug': 'clia',
                'company_type': 'CLIA',
                'email': 'contato@clia.com.br',
                'phone': '+55 71 3366-6000',
                'website': 'https://www.clia.com.br',
                'address': 'Centro Logístico e Industrial de Aratu',
                'city': 'Simões Filho',
                'state': 'BA',
                'zip_code': '43700-000',
                'country': 'Brasil',
                'primary_color': '#006633',
                'secondary_color': '#009966',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for company_data in companies_data:
            company, created = Company.objects.update_or_create(
                slug=company_data['slug'],
                defaults=company_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Empresa "{company.name}" criada com sucesso!')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'• Empresa "{company.name}" atualizada.')
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Resumo ==='))
        self.stdout.write(self.style.SUCCESS(f'Empresas criadas: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Empresas atualizadas: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'Total: {created_count + updated_count}'))
