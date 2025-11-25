"""
Models for Container Structure and Damage inspection
Specific models for container parts and damage types
"""
from django.db import models
from apps.core.models import Company, User, BaseModel
from apps.inspections.models import Inspection


class ContainerStructure(BaseModel):
    """
    Physical parts/components of a container to be inspected
    Based on the ESTRUTURA list (64 items)
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='container_structures')
    
    code = models.CharField(max_length=10)  # e.g., "1", "2", etc.
    name = models.CharField(max_length=200)  # e.g., "ALAVANCA DA HASTE"
    description = models.TextField(blank=True)
    
    # Grouping
    GROUP_CHOICES = [
        ('STRUCTURAL', 'Estrutural'),
        ('DOOR', 'Porta/Trave'),
        ('ROOF', 'Teto'),
        ('FLOOR', 'Assoalho'),
        ('WALL', 'Paredes'),
        ('CORNER', 'Cantos'),
        ('REEFER', 'Refrigeração'),
        ('IDENTIFICATION', 'Identificação'),
        ('OTHER', 'Outros'),
    ]
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='OTHER')
    
    # Configuration
    is_critical = models.BooleanField(default=False)  # Critical component
    requires_photo = models.BooleanField(default=False)  # Always requires photo
    is_active = models.BooleanField(default=True)
    
    # Ordering
    sequence = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sequence', 'code']
        unique_together = ['company', 'code']
        verbose_name = 'Estrutura do Container'
        verbose_name_plural = 'Estruturas do Container'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class DamageType(BaseModel):
    """
    Types of damage/problems that can be found
    Based on the AVARIA list (46 items)
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='damage_types')
    
    code = models.CharField(max_length=10)  # e.g., "1", "2", etc.
    name = models.CharField(max_length=200)  # e.g., "AMASSADO(A)"
    description = models.TextField(blank=True)
    
    # Severity classification
    SEVERITY_CHOICES = [
        ('MINOR', 'Leve'),
        ('MODERATE', 'Moderado'),
        ('MAJOR', 'Grave'),
        ('CRITICAL', 'Crítico'),
    ]
    default_severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MODERATE')
    
    # Impact
    affects_operation = models.BooleanField(default=False)  # Affects container operation
    requires_repair = models.BooleanField(default=True)  # Requires repair
    
    # Configuration
    requires_photo = models.BooleanField(default=True)  # Always requires photo evidence
    requires_measurement = models.BooleanField(default=False)  # Requires dimensions
    is_active = models.BooleanField(default=True)
    
    # Color coding for UI
    color = models.CharField(max_length=7, default='#FFA500')  # Orange default
    
    # Ordering
    sequence = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sequence', 'code']
        unique_together = ['company', 'code']
        verbose_name = 'Tipo de Avaria'
        verbose_name_plural = 'Tipos de Avaria'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class StructureInspectionItem(BaseModel):
    """
    Individual inspection of a container structure part
    Links Inspection + Structure + Damage (if any)
    """
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='structure_items')
    structure = models.ForeignKey(ContainerStructure, on_delete=models.PROTECT, related_name='inspection_items')
    
    # Inspection result
    STATUS_CHOICES = [
        ('OK', 'OK - Sem Avaria'),
        ('DAMAGED', 'Avariado'),
        ('NOT_INSPECTED', 'Não Inspecionado'),
        ('NOT_APPLICABLE', 'Não Aplicável'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_INSPECTED')
    
    # If damaged
    damage_type = models.ForeignKey(DamageType, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspection_items')
    
    # Details
    notes = models.TextField(blank=True)
    
    # Measurements (if applicable)
    measurement_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='cm')
    measurement_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='cm')
    measurement_depth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='cm')
    
    # Location on structure (for precise damage location)
    location_description = models.CharField(max_length=200, blank=True)  # e.g., "Canto superior esquerdo"
    
    # Photo reference
    has_photo = models.BooleanField(default=False)
    photo_count = models.IntegerField(default=0)
    
    # Inspector
    inspected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    inspected_at = models.DateTimeField(null=True, blank=True)
    
    # Severity override (can override damage_type default)
    severity_override = models.CharField(max_length=20, choices=DamageType.SEVERITY_CHOICES, blank=True)
    
    class Meta:
        ordering = ['structure__sequence', 'created_at']
        unique_together = ['inspection', 'structure']
        verbose_name = 'Item de Inspeção'
        verbose_name_plural = 'Itens de Inspeção'
    
    def __str__(self):
        return f"{self.inspection.reference_number} - {self.structure.name}"
    
    @property
    def final_severity(self):
        """Returns the final severity (override or default from damage type)"""
        if self.severity_override:
            return self.severity_override
        if self.damage_type:
            return self.damage_type.default_severity
        return 'MINOR' if self.status == 'OK' else None


class StructureInspectionPhoto(BaseModel):
    """
    Photos specific to a structure inspection item
    Links to both the main inspection photo and the specific structure item
    """
    from apps.inspections.models import InspectionPhoto
    
    structure_item = models.ForeignKey(StructureInspectionItem, on_delete=models.CASCADE, related_name='photos')
    photo = models.ForeignKey(InspectionPhoto, on_delete=models.CASCADE, related_name='structure_items')
    
    # Annotation on photo (to mark specific damage location)
    annotation_x = models.IntegerField(null=True, blank=True)  # X coordinate
    annotation_y = models.IntegerField(null=True, blank=True)  # Y coordinate
    annotation_text = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Foto da Estrutura'
        verbose_name_plural = 'Fotos das Estruturas'
    
    def __str__(self):
        return f"Photo for {self.structure_item}"


class InspectionChecklist(BaseModel):
    """
    Predefined checklist for systematic inspection
    Can be based on container type or customer requirements
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='inspection_checklists')
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Apply to
    CONTAINER_TYPES = [
        ('DRY', 'Dry Container'),
        ('REEFER', 'Reefer'),
        ('OPEN_TOP', 'Open Top'),
        ('FLAT_RACK', 'Flat Rack'),
        ('TANK', 'Tank'),
        ('ALL', 'All Types'),
    ]
    container_type = models.CharField(max_length=20, choices=CONTAINER_TYPES, default='ALL')
    
    # Structures to inspect
    structures = models.ManyToManyField(ContainerStructure, through='ChecklistStructure')
    
    # Configuration
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Usage stats
    usage_count = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_checklists')
    
    class Meta:
        ordering = ['-is_default', 'name']
        verbose_name = 'Checklist de Inspeção'
        verbose_name_plural = 'Checklists de Inspeção'
    
    def __str__(self):
        return f"{self.name} ({self.container_type})"


class ChecklistStructure(models.Model):
    """Through model for Checklist and Structure relationship"""
    checklist = models.ForeignKey(InspectionChecklist, on_delete=models.CASCADE)
    structure = models.ForeignKey(ContainerStructure, on_delete=models.CASCADE)
    
    sequence = models.IntegerField(default=0)
    is_required = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['sequence']
        unique_together = ['checklist', 'structure']
    
    def __str__(self):
        return f"{self.checklist.name} - {self.structure.name}"
