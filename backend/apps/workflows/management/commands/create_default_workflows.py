"""
Management command to create default workflows for each inspection type
"""
from django.core.management.base import BaseCommand
from apps.core.models import Company
from apps.inspections.models import InspectionType
from apps.workflows.models import Workflow, WorkflowStep, Form, FormField


class Command(BaseCommand):
    help = 'Create default workflows for inspection types'

    def handle(self, *args, **kwargs):
        companies = Company.objects.all()
        
        for company in companies:
            self.stdout.write(f'Creating workflows for {company.name}...')
            
            # Get or create inspection types
            cargo_type, _ = InspectionType.objects.get_or_create(
                company=company,
                code='CARGO',
                defaults={
                    'name': 'Inspeção de Carga',
                    'description': 'Inspeção de carga geral',
                    'icon': 'package',
                    'color': '#0066CC'
                }
            )
            
            container_type, _ = InspectionType.objects.get_or_create(
                company=company,
                code='CONTAINER',
                defaults={
                    'name': 'Inspeção de Container',
                    'description': 'Inspeção de containers marítimos',
                    'icon': 'container',
                    'color': '#00AA66'
                }
            )
            
            vehicle_type, _ = InspectionType.objects.get_or_create(
                company=company,
                code='VEHICLE',
                defaults={
                    'name': 'Inspeção de Veículo',
                    'description': 'Inspeção de veículos e caminhões',
                    'icon': 'truck',
                    'color': '#FF6600'
                }
            )
            
            # Create Container Inspection Workflow
            self.create_container_workflow(company, container_type)
            
            # Create Cargo Inspection Workflow
            self.create_cargo_workflow(company, cargo_type)
            
            # Create Vehicle Inspection Workflow
            self.create_vehicle_workflow(company, vehicle_type)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Workflows created for {company.name}'))

    def create_container_workflow(self, company, inspection_type):
        """Create default container inspection workflow"""
        workflow, created = Workflow.objects.get_or_create(
            company=company,
            inspection_type=inspection_type,
            name='Inspeção Padrão de Container',
            defaults={
                'description': 'Workflow completo para inspeção de containers',
                'is_default': True,
                'is_active': True
            }
        )
        
        if not created:
            return
        
        # Step 1: Identificação
        step1 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Identificação do Container',
            description='Registre os dados de identificação do container',
            step_type='FORM',
            sequence_order=1,
            is_required=True
        )
        
        form1 = Form.objects.create(
            company=company,
            name='Identificação do Container',
            description='Dados básicos do container'
        )
        step1.form = form1
        step1.save()
        
        FormField.objects.bulk_create([
            FormField(form=form1, label='Número do Container', field_type='TEXT', is_required=True, sequence_order=1),
            FormField(form=form1, label='Número do Lacre', field_type='TEXT', is_required=True, sequence_order=2),
            FormField(form=form1, label='Tipo de Container', field_type='SELECT', is_required=True, sequence_order=3,
                     options={'choices': ['20ft Standard', '40ft Standard', '40ft High Cube', '20ft Refrigerated', '40ft Refrigerated']}),
        ])
        
        # Step 2: Fotos Externas
        step2 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Fotos Externas',
            description='Tire fotos de todos os lados externos do container',
            step_type='PHOTO',
            sequence_order=2,
            is_required=True,
            min_photos=4,
            max_photos=20
        )
        
        # Step 3: Inspeção Estrutural
        step3 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Inspeção Estrutural',
            description='Verifique a estrutura e condições do container',
            step_type='FORM',
            sequence_order=3,
            is_required=True
        )
        
        form3 = Form.objects.create(
            company=company,
            name='Inspeção Estrutural',
            description='Checklist estrutural do container'
        )
        step3.form = form3
        step3.save()
        
        FormField.objects.bulk_create([
            FormField(form=form3, label='Condição das Paredes', field_type='SELECT', is_required=True, sequence_order=1,
                     options={'choices': ['Excelente', 'Boa', 'Regular', 'Ruim']}),
            FormField(form=form3, label='Condição do Piso', field_type='SELECT', is_required=True, sequence_order=2,
                     options={'choices': ['Excelente', 'Boa', 'Regular', 'Ruim']}),
            FormField(form=form3, label='Condição do Teto', field_type='SELECT', is_required=True, sequence_order=3,
                     options={'choices': ['Excelente', 'Boa', 'Regular', 'Ruim']}),
            FormField(form=form3, label='Portas Funcionando', field_type='BOOLEAN', is_required=True, sequence_order=4),
            FormField(form=form3, label='Vazamentos Detectados', field_type='BOOLEAN', is_required=True, sequence_order=5),
            FormField(form=form3, label='Observações', field_type='TEXTAREA', is_required=False, sequence_order=6),
        ])
        
        # Step 4: Fotos Internas
        step4 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Fotos Internas',
            description='Tire fotos do interior do container',
            step_type='PHOTO',
            sequence_order=4,
            is_required=True,
            min_photos=3,
            max_photos=15
        )
        
        # Step 5: Danos e Avarias
        step5 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Registro de Danos',
            description='Registre qualquer dano ou avaria encontrada',
            step_type='FORM',
            sequence_order=5,
            is_required=False
        )
        
        form5 = Form.objects.create(
            company=company,
            name='Registro de Danos',
            description='Documentação de danos e avarias'
        )
        step5.form = form5
        step5.save()
        
        FormField.objects.bulk_create([
            FormField(form=form5, label='Tipo de Dano', field_type='SELECT', is_required=True, sequence_order=1,
                     options={'choices': ['Amassado', 'Corrosão', 'Furo', 'Rachadura', 'Outro']}),
            FormField(form=form5, label='Localização', field_type='TEXT', is_required=True, sequence_order=2),
            FormField(form=form5, label='Severidade', field_type='SELECT', is_required=True, sequence_order=3,
                     options={'choices': ['Leve', 'Moderada', 'Grave', 'Crítica']}),
            FormField(form=form5, label='Descrição Detalhada', field_type='TEXTAREA', is_required=True, sequence_order=4),
        ])

    def create_cargo_workflow(self, company, inspection_type):
        """Create default cargo inspection workflow"""
        workflow, created = Workflow.objects.get_or_create(
            company=company,
            inspection_type=inspection_type,
            name='Inspeção Padrão de Carga',
            defaults={
                'description': 'Workflow para inspeção de carga geral',
                'is_default': True,
                'is_active': True
            }
        )
        
        if not created:
            return
        
        # Step 1: Identificação da Carga
        step1 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Identificação da Carga',
            description='Registre os dados da carga',
            step_type='FORM',
            sequence_order=1,
            is_required=True
        )
        
        form1 = Form.objects.create(
            company=company,
            name='Identificação da Carga',
            description='Dados básicos da carga'
        )
        step1.form = form1
        step1.save()
        
        FormField.objects.bulk_create([
            FormField(form=form1, label='Descrição da Carga', field_type='TEXTAREA', is_required=True, sequence_order=1),
            FormField(form=form1, label='Quantidade de Volumes', field_type='NUMBER', is_required=True, sequence_order=2),
            FormField(form=form1, label='Peso Total (kg)', field_type='NUMBER', is_required=True, sequence_order=3),
            FormField(form=form1, label='Tipo de Embalagem', field_type='SELECT', is_required=True, sequence_order=4,
                     options={'choices': ['Caixas', 'Paletes', 'Sacos', 'Tambores', 'Granel', 'Outro']}),
        ])
        
        # Step 2: Fotos Gerais
        WorkflowStep.objects.create(
            workflow=workflow,
            name='Fotos Gerais da Carga',
            description='Tire fotos gerais da carga',
            step_type='PHOTO',
            sequence_order=2,
            is_required=True,
            min_photos=3,
            max_photos=20
        )
        
        # Step 3: Verificação de Condições
        step3 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Verificação de Condições',
            description='Verifique as condições da carga',
            step_type='FORM',
            sequence_order=3,
            is_required=True
        )
        
        form3 = Form.objects.create(
            company=company,
            name='Condições da Carga',
            description='Checklist de condições'
        )
        step3.form = form3
        step3.save()
        
        FormField.objects.bulk_create([
            FormField(form=form3, label='Embalagem Intacta', field_type='BOOLEAN', is_required=True, sequence_order=1),
            FormField(form=form3, label='Sinais de Umidade', field_type='BOOLEAN', is_required=True, sequence_order=2),
            FormField(form=form3, label='Produtos Danificados', field_type='BOOLEAN', is_required=True, sequence_order=3),
            FormField(form=form3, label='Etiquetas Legíveis', field_type='BOOLEAN', is_required=True, sequence_order=4),
            FormField(form=form3, label='Observações', field_type='TEXTAREA', is_required=False, sequence_order=5),
        ])

    def create_vehicle_workflow(self, company, inspection_type):
        """Create default vehicle inspection workflow"""
        workflow, created = Workflow.objects.get_or_create(
            company=company,
            inspection_type=inspection_type,
            name='Inspeção Padrão de Veículo',
            defaults={
                'description': 'Workflow para inspeção de veículos',
                'is_default': True,
                'is_active': True
            }
        )
        
        if not created:
            return
        
        # Step 1: Identificação do Veículo
        step1 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Identificação do Veículo',
            description='Registre os dados do veículo',
            step_type='FORM',
            sequence_order=1,
            is_required=True
        )
        
        form1 = Form.objects.create(
            company=company,
            name='Identificação do Veículo',
            description='Dados básicos do veículo'
        )
        step1.form = form1
        step1.save()
        
        FormField.objects.bulk_create([
            FormField(form=form1, label='Placa', field_type='TEXT', is_required=True, sequence_order=1),
            FormField(form=form1, label='Modelo', field_type='TEXT', is_required=True, sequence_order=2),
            FormField(form=form1, label='Ano', field_type='NUMBER', is_required=True, sequence_order=3),
            FormField(form=form1, label='Cor', field_type='TEXT', is_required=True, sequence_order=4),
            FormField(form=form1, label='Chassi (VIN)', field_type='TEXT', is_required=False, sequence_order=5),
        ])
        
        # Step 2: Fotos Externas
        WorkflowStep.objects.create(
            workflow=workflow,
            name='Fotos Externas',
            description='Tire fotos de todos os ângulos do veículo',
            step_type='PHOTO',
            sequence_order=2,
            is_required=True,
            min_photos=6,
            max_photos=20
        )
        
        # Step 3: Inspeção Visual
        step3 = WorkflowStep.objects.create(
            workflow=workflow,
            name='Inspeção Visual',
            description='Verifique as condições visuais do veículo',
            step_type='FORM',
            sequence_order=3,
            is_required=True
        )
        
        form3 = Form.objects.create(
            company=company,
            name='Inspeção Visual do Veículo',
            description='Checklist visual'
        )
        step3.form = form3
        step3.save()
        
        FormField.objects.bulk_create([
            FormField(form=form3, label='Condição da Pintura', field_type='SELECT', is_required=True, sequence_order=1,
                     options={'choices': ['Excelente', 'Boa', 'Regular', 'Ruim']}),
            FormField(form=form3, label='Pneus em Bom Estado', field_type='BOOLEAN', is_required=True, sequence_order=2),
            FormField(form=form3, label='Vidros Intactos', field_type='BOOLEAN', is_required=True, sequence_order=3),
            FormField(form=form3, label='Faróis Funcionando', field_type='BOOLEAN', is_required=True, sequence_order=4),
            FormField(form=form3, label='Amassados ou Arranhões', field_type='BOOLEAN', is_required=True, sequence_order=5),
            FormField(form=form3, label='Observações', field_type='TEXTAREA', is_required=False, sequence_order=6),
        ])
