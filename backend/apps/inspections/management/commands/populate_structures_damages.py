"""
Management command to populate Container Structures and Damage Types
Usage: python manage.py populate_structures_damages
"""
from django.core.management.base import BaseCommand
from apps.core.models import Company
from apps.inspections.structure_models import ContainerStructure, DamageType


class Command(BaseCommand):
    help = 'Popula estruturas e tipos de avaria para todas as empresas'

    # Lista de Estruturas (64 itens)
    STRUCTURES = [
        (1, "ALAVANCA DA HASTE", "DOOR"),
        (2, "ANEL DA HASTE", "DOOR"),
        (3, "ASSOALHO", "FLOOR"),
        (4, "BARRA J", "STRUCTURAL"),
        (5, "BOLSA", "OTHER"),
        (6, "BORRACHA/VEDAÇÃO", "DOOR"),
        (7, "CABO DE LONA", "ROOF"),
        (8, "CABO ELÉTRICO (RF)", "REEFER"),
        (9, "CARGA EM FLAT RACK/OPEN TOP", "OTHER"),
        (10, "CINTA", "OTHER"),
        (11, "COL. DIREITA FRENTE", "WALL"),
        (12, "COL. DIREITA PORTA/TRAS.", "WALL"),
        (13, "COL. ESQUERDA FRENTE", "WALL"),
        (14, "COL. ESQUERDA PORTA/TRAS.", "WALL"),
        (15, "COMPARTIMENTO DO CABO (RF)", "REEFER"),
        (16, "CONTAINER", "STRUCTURAL"),
        (17, "DISPLAY (RF)", "REEFER"),
        (18, "DISPOSITIVO DE CANTO", "CORNER"),
        (19, "DIVERGENTE", "IDENTIFICATION"),
        (20, "DOBRADIÇA", "DOOR"),
        (21, "ESCADA (TK)", "STRUCTURAL"),
        (22, "FRENTE", "WALL"),
        (23, "FUNDO", "WALL"),
        (24, "HASTE", "DOOR"),
        (25, "LACRE", "IDENTIFICATION"),
        (26, "LADO DIREITO", "WALL"),
        (27, "LADO DIREITO E ESQUERDO", "WALL"),
        (28, "LADO DIREITO E FRENTE", "WALL"),
        (29, "LADO DIREITO, ESQUERDO, FRENTE", "WALL"),
        (30, "LADO ESQUERDO", "WALL"),
        (31, "LADO ESQUERDO E FRENTE", "WALL"),
        (32, "LONA", "ROOF"),
        (33, "LONG. INF. DIREITA", "STRUCTURAL"),
        (34, "LONG. INF. ESQUERDA", "STRUCTURAL"),
        (35, "LONG. INF. FRENTE", "STRUCTURAL"),
        (36, "LONG. INF. PORTA/TRAS.", "STRUCTURAL"),
        (37, "LONG. SUP. PORTA/TRAS.", "STRUCTURAL"),
        (38, "LONG. SUP. DIREITA", "STRUCTURAL"),
        (39, "LONG. SUP. ESQUERDA", "STRUCTURAL"),
        (40, "LONG. SUP. FRENTE", "STRUCTURAL"),
        (41, "MICRO LINK (RF)", "REEFER"),
        (42, "MOLA (FR)", "STRUCTURAL"),
        (43, "MOTOR/MAQUINÁRIO (RF)", "REEFER"),
        (44, "NUMERAÇÃO / IDENTIFICAÇÃO", "IDENTIFICATION"),
        (45, "PAINEL DE CONTROLE", "REEFER"),
        (46, "PASSADIÇO", "STRUCTURAL"),
        (47, "PLACA DE IDENTIFICAÇÃO", "IDENTIFICATION"),
        (48, "PLACA MÃE (RF)", "REEFER"),
        (49, "PORTA OU TRASEIRA", "DOOR"),
        (50, "RETENTOR DA ALAVANCA", "DOOR"),
        (51, "RETENTOR DA UNHA/TRAVA", "DOOR"),
        (52, "SUPORTE DA HASTE", "DOOR"),
        (53, "TAMPA", "OTHER"),
        (54, "TAMPA CONDENSADOR", "REEFER"),
        (55, "TAMPA EVAPORADOR", "REEFER"),
        (56, "TAMPA PAINEL", "REEFER"),
        (57, "TETO", "ROOF"),
        (58, "TOMADA (RF)", "REEFER"),
        (59, "TRAVA DA TAMPA (FR)", "STRUCTURAL"),
        (60, "TRAVESSA DE FUNDO", "FLOOR"),
        (61, "TRAVESSA DE TETO (OT)", "ROOF"),
        (62, "UNHA/TRAVE DA HASTE", "DOOR"),
        (63, "VÁLVULA", "OTHER"),
        (64, "VENTILADOR", "REEFER"),
    ]

    # Lista de Avarias (46 itens) com severidade e configurações
    DAMAGES = [
        (1, "AMASSADO(A)", "MODERATE", False, True, "#FFA500"),
        (2, "AMASSADO(A) GRAVE", "MAJOR", True, True, "#FF6600"),
        (3, "ARRANHADO(A)", "MINOR", False, True, "#FFD700"),
        (4, "CORTADO(A)", "MAJOR", True, True, "#FF4500"),
        (5, "DIVERGÊNCIA DE PESO", "MODERATE", False, False, "#FF8C00"),
        (6, "EMBALAGEM SUJA", "MINOR", False, False, "#DEB887"),
        (7, "EMPENADO(A)", "MODERATE", True, True, "#FFA500"),
        (8, "ENFERRUJADO(A)", "MODERATE", False, True, "#CD853F"),
        (9, "ENFERRUJADO(A) GRAVE", "MAJOR", True, True, "#8B4513"),
        (10, "ENTREABERTO(A)", "MODERATE", True, True, "#FF8C00"),
        (11, "ESTUFADO(A)", "MODERATE", False, True, "#FFA07A"),
        (12, "ESTUFADO(A) GRAVE", "MAJOR", True, True, "#FF6347"),
        (13, "FALTANDO", "CRITICAL", True, True, "#DC143C"),
        (14, "FURADO(A)", "MAJOR", True, True, "#FF0000"),
        (15, "ILEGÍVEL", "MINOR", False, True, "#FFD700"),
        (16, "LACRE DIVERGENTE", "MAJOR", True, True, "#FF6600"),
        (17, "LACRE IMPRÓPRIO", "MODERATE", True, True, "#FFA500"),
        (18, "LACRE ROMPIDO", "CRITICAL", True, True, "#DC143C"),
        (19, "MAL ESTADO DE CONSERVAÇÃO", "MODERATE", False, True, "#CD853F"),
        (20, "MAL ESTADO DE CONSERVAÇÃO GRAVE", "MAJOR", True, True, "#8B4513"),
        (21, "MANCHA DE ÓLEO", "MODERATE", False, True, "#696969"),
        (22, "MANCHADO/ARRANHADO/QUEBRADO", "MAJOR", True, True, "#FF6347"),
        (23, "MARCA DE PLACAR IMO", "MINOR", False, True, "#FFD700"),
        (24, "MOLHADA - FR", "MODERATE", False, True, "#4682B4"),
        (25, "MOLHADO(A)", "MODERATE", False, True, "#4682B4"),
        (26, "MOLHADO(A) E ENFERRUJADO(A)", "MAJOR", True, True, "#8B4513"),
        (27, "PEAÇÃO IMPRÓPRIA - FR", "MAJOR", True, True, "#FF6600"),
        (28, "PICHADO", "MINOR", False, True, "#A9A9A9"),
        (29, "QUEBRADO", "MAJOR", True, True, "#FF4500"),
        (30, "QUEBRADO(A)", "MAJOR", True, True, "#FF4500"),
        (31, "QUEBRADO(A) E ARRANHADO(A)", "MAJOR", True, True, "#FF6347"),
        (32, "QUEBRADO(A) E ENFERRUJADO(A)", "MAJOR", True, True, "#8B4513"),
        (33, "RASGADO(A)", "MAJOR", True, True, "#FF6600"),
        (34, "RASGADO(A) E VAZANDO", "CRITICAL", True, True, "#DC143C"),
        (35, "REMENDADO(A)", "MINOR", False, True, "#DEB887"),
        (36, "REMENDO MAL FEITO/GRANDE", "MODERATE", False, True, "#CD853F"),
        (37, "REMENDO PROVISÓRIO", "MODERATE", True, True, "#FFA500"),
        (38, "SEM AVARIA", "MINOR", False, False, "#32CD32"),
        (39, "SEM IDENTIFICAÇÃO", "MODERATE", False, True, "#FFA500"),
        (40, "SEM LACRE", "CRITICAL", True, True, "#DC143C"),
        (41, "SEM LACRE DE PAINEL", "MAJOR", True, True, "#FF6600"),
        (42, "SOLTA(O)", "MODERATE", True, True, "#FFA500"),
        (43, "SUJO(A)/RASGADO(A)/ABERTO(A)", "MAJOR", True, True, "#FF6347"),
        (44, "TORCIDO(A)", "MODERATE", True, True, "#FFA500"),
        (45, "TWIST-LOCK (FR)", "MODERATE", True, True, "#FFA500"),
        (46, "VAZANDO", "CRITICAL", True, True, "#DC143C"),
    ]

    def handle(self, *args, **options):
        companies = Company.objects.all()
        
        if not companies.exists():
            self.stdout.write(self.style.ERROR('Nenhuma empresa encontrada. Execute create_companies primeiro.'))
            return

        for company in companies:
            self.stdout.write(f'\nProcessando empresa: {company.name}')
            
            # Populate Structures
            self.stdout.write('Criando estruturas...')
            created_structures = 0
            for code, name, group in self.STRUCTURES:
                structure, created = ContainerStructure.objects.get_or_create(
                    company=company,
                    code=str(code),
                    defaults={
                        'name': name,
                        'group': group,
                        'sequence': code,
                        'is_critical': group in ['STRUCTURAL', 'DOOR', 'CORNER'],
                        'requires_photo': group in ['REEFER', 'IDENTIFICATION'],
                    }
                )
                if created:
                    created_structures += 1
            
            self.stdout.write(self.style.SUCCESS(f'✓ {created_structures} estruturas criadas'))
            
            # Populate Damage Types
            self.stdout.write('Criando tipos de avaria...')
            created_damages = 0
            for code, name, severity, affects_op, req_repair, color in self.DAMAGES:
                damage, created = DamageType.objects.get_or_create(
                    company=company,
                    code=str(code),
                    defaults={
                        'name': name,
                        'default_severity': severity,
                        'affects_operation': affects_op,
                        'requires_repair': req_repair,
                        'color': color,
                        'sequence': code,
                        'requires_photo': True,
                        'requires_measurement': severity in ['MAJOR', 'CRITICAL'],
                    }
                )
                if created:
                    created_damages += 1
            
            self.stdout.write(self.style.SUCCESS(f'✓ {created_damages} tipos de avaria criados'))

        self.stdout.write(self.style.SUCCESS('\n✅ Processo concluído com sucesso!'))
        self.stdout.write(f'Total de empresas processadas: {companies.count()}')
