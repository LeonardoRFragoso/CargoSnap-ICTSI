"""
Management command to create superuser with company
Usage: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from apps.core.models import Company, User


class Command(BaseCommand):
    help = 'Cria um superusuário admin com empresa'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Criar Superusuário ===\n'))
        
        # Listar empresas
        companies = Company.objects.all()
        if not companies.exists():
            self.stdout.write(self.style.ERROR('Nenhuma empresa encontrada. Execute create_companies primeiro.'))
            return
        
        self.stdout.write('Empresas disponíveis:')
        for i, company in enumerate(companies, 1):
            self.stdout.write(f'  {i}. {company.name} ({company.company_type})')
        
        # Escolher empresa
        while True:
            try:
                choice = input('\nEscolha a empresa (1-{}): '.format(companies.count()))
                choice = int(choice)
                if 1 <= choice <= companies.count():
                    company = list(companies)[choice - 1]
                    break
                else:
                    self.stdout.write(self.style.ERROR('Escolha inválida.'))
            except (ValueError, KeyboardInterrupt):
                self.stdout.write(self.style.ERROR('\nOperação cancelada.'))
                return
        
        # Dados do usuário
        username = input('\nUsuário: ')
        email = input('Email: ')
        first_name = input('Primeiro Nome: ')
        last_name = input('Sobrenome: ')
        
        import getpass
        while True:
            password = getpass.getpass('Senha: ')
            password2 = getpass.getpass('Confirme a senha: ')
            if password == password2:
                break
            else:
                self.stdout.write(self.style.ERROR('Senhas não coincidem. Tente novamente.'))
        
        # Criar superusuário
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                company=company,
                role='ADMIN'
            )
            self.stdout.write(self.style.SUCCESS(f'\n✅ Superusuário "{username}" criado com sucesso!'))
            self.stdout.write(f'   Empresa: {company.name}')
            self.stdout.write(f'   Email: {email}')
            self.stdout.write(f'   Role: ADMIN')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Erro ao criar usuário: {e}'))
