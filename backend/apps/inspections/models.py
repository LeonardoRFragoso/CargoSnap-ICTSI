"""
Models for Inspections app
Complete inspection system with photos, videos, forms, and documentation
"""
from django.db import models
from django.core.validators import FileExtensionValidator
from apps.core.models import User, Company, BaseModel


class InspectionType(BaseModel):
    """Types of inspections (Cargo, Container, Vehicle, etc.)"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='inspection_types')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon name for UI
    color = models.CharField(max_length=7, default='#0066CC')  # Hex color
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['company', 'code']
    
    def __str__(self):
        return f"{self.name} ({self.company.company_type})"


class Inspection(BaseModel):
    """Main inspection record"""
    STATUS_CHOICES = [
        ('DRAFT', 'Rascunho'),
        ('IN_PROGRESS', 'Em Andamento'),
        ('COMPLETED', 'Concluída'),
        ('APPROVED', 'Aprovada'),
        ('REJECTED', 'Rejeitada'),
        ('CANCELLED', 'Cancelada'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='inspections')
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.PROTECT, related_name='inspections')
    
    # Reference information
    reference_number = models.CharField(max_length=100, unique=True)
    external_reference = models.CharField(max_length=100, blank=True)  # Customer reference
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Status and assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_inspections')
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_inspections')
    
    # Location and environment
    location = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    weather_condition = models.CharField(max_length=50, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Dates
    scheduled_date = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Customer/Client information
    customer_name = models.CharField(max_length=200, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Container/Cargo specific fields
    container_number = models.CharField(max_length=50, blank=True, help_text='Container number (e.g., ABCD1234567)')
    seal_number = models.CharField(max_length=50, blank=True, help_text='Seal/Lock number')
    booking_number = models.CharField(max_length=100, blank=True, help_text='Booking or BL number')
    vessel_name = models.CharField(max_length=200, blank=True, help_text='Vessel/Ship name')
    voyage_number = models.CharField(max_length=50, blank=True, help_text='Voyage number')
    container_type = models.CharField(max_length=50, blank=True, help_text='Container type (20ft, 40ft, etc.)')
    container_size = models.CharField(max_length=20, blank=True, help_text='Container size')
    cargo_description = models.TextField(blank=True, help_text='Description of cargo/goods')
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Cargo weight in kg')
    
    # Vehicle specific fields
    vehicle_plate = models.CharField(max_length=20, blank=True, help_text='Vehicle license plate')
    vehicle_model = models.CharField(max_length=100, blank=True, help_text='Vehicle model')
    vehicle_year = models.IntegerField(null=True, blank=True, help_text='Vehicle year')
    vehicle_vin = models.CharField(max_length=50, blank=True, help_text='Vehicle VIN number')
    
    # CargoSnap Integration
    cargosnap_file = models.ForeignKey(
        'cargosnap_integration.CargoSnapFile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inspections',
        help_text='Arquivo CargoSnap vinculado a esta inspeção'
    )
    imported_from_cargosnap = models.BooleanField(
        default=False,
        help_text='Indica se esta inspeção foi importada do CargoSnap'
    )
    
    # Additional data (JSON for flexibility)
    custom_fields = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['reference_number']),
            models.Index(fields=['assigned_to', 'status']),
        ]
    
    def __str__(self):
        return f"{self.reference_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Auto-generate reference number if not provided
        if not self.reference_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.reference_number = f"{self.company.company_type}-{timestamp}"
        super().save(*args, **kwargs)


class InspectionPhoto(BaseModel):
    """Photos taken during inspection"""
    PHOTO_SOURCE_CHOICES = [
        ('MOBILE', 'Câmera Mobile'),
        ('UPLOAD', 'Upload Manual'),
        ('CARGOSNAP', 'CargoSnap'),
    ]
    
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='photos')
    
    # File information
    photo = models.ImageField(upload_to='inspections/photos/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='inspections/thumbnails/%Y/%m/%d/', blank=True)
    
    # Photo metadata
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    caption = models.CharField(max_length=500, blank=True)
    photo_source = models.CharField(max_length=20, choices=PHOTO_SOURCE_CHOICES, default='MOBILE')
    
    # Technical data
    taken_at = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    device_info = models.JSONField(default=dict, blank=True)  # Camera, phone model, etc.
    
    # CargoSnap Integration
    cargosnap_upload = models.ForeignKey(
        'cargosnap_integration.CargoSnapUpload',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inspection_photos',
        help_text='Upload CargoSnap de origem desta foto'
    )
    
    # Organization
    sequence_number = models.IntegerField(default=0)
    is_cover_photo = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sequence_number', 'created_at']
    
    def __str__(self):
        return f"Photo {self.sequence_number} - {self.inspection.reference_number}"


class InspectionVideo(BaseModel):
    """Videos taken during inspection"""
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='videos')
    
    # File information
    video = models.FileField(
        upload_to='inspections/videos/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])]
    )
    thumbnail = models.ImageField(upload_to='inspections/video_thumbnails/%Y/%m/%d/', blank=True)
    
    # Video metadata
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    duration_seconds = models.IntegerField(default=0)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Technical data
    taken_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Video - {self.inspection.reference_number}"


class InspectionDocument(BaseModel):
    """Additional documents attached to inspection"""
    DOCUMENT_TYPES = [
        ('PDF', 'PDF Document'),
        ('EXCEL', 'Excel Spreadsheet'),
        ('WORD', 'Word Document'),
        ('IMAGE', 'Image'),
        ('OTHER', 'Other'),
    ]
    
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='documents')
    
    # File information
    document = models.FileField(upload_to='inspections/documents/%Y/%m/%d/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='OTHER')
    
    # Document metadata
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_size_mb = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.title} - {self.inspection.reference_number}"


class InspectionTag(BaseModel):
    """Tags/Labels for organizing inspections"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='inspection_tags')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#0066CC')
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['company', 'name']
    
    def __str__(self):
        return self.name


class InspectionTagRelation(models.Model):
    """Many-to-many relationship between Inspections and Tags"""
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='tag_relations')
    tag = models.ForeignKey(InspectionTag, on_delete=models.CASCADE, related_name='inspection_relations')
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['inspection', 'tag']
    
    def __str__(self):
        return f"{self.inspection.reference_number} - {self.tag.name}"


class InspectionSignature(BaseModel):
    """Digital signatures for inspections"""
    SIGNATURE_TYPES = [
        ('INSPECTOR', 'Inspector'),
        ('SUPERVISOR', 'Supervisor'),
        ('CUSTOMER', 'Customer'),
        ('WITNESS', 'Witness'),
    ]
    
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='signatures')
    signature_type = models.CharField(max_length=20, choices=SIGNATURE_TYPES)
    
    # Signature data
    signature_image = models.ImageField(upload_to='inspections/signatures/%Y/%m/%d/')
    signer_name = models.CharField(max_length=200)
    signer_email = models.EmailField(blank=True)
    signer_role = models.CharField(max_length=100, blank=True)
    
    # Metadata
    signed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['signed_at']
    
    def __str__(self):
        return f"{self.signer_name} ({self.signature_type}) - {self.inspection.reference_number}"


class InspectionComment(BaseModel):
    """Comments and notes on inspections"""
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='inspection_comments')
    
    comment = models.TextField()
    is_internal = models.BooleanField(default=True)  # Internal vs customer-visible
    
    # For threaded comments
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user} on {self.inspection.reference_number}"


class ScannedReference(BaseModel):
    """Scanned barcodes, QR codes, license plates, etc."""
    REFERENCE_TYPES = [
        ('BARCODE', 'Barcode'),
        ('QR_CODE', 'QR Code'),
        ('LICENSE_PLATE', 'License Plate'),
        ('CONTAINER_NUMBER', 'Container Number'),
        ('SEAL_NUMBER', 'Seal Number'),
        ('OTHER', 'Other'),
    ]
    
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='scanned_references')
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPES)
    
    # Scanned data
    value = models.CharField(max_length=200)
    raw_data = models.TextField(blank=True)  # Raw scan data
    
    # Validation
    is_valid = models.BooleanField(default=True)
    validation_message = models.TextField(blank=True)
    
    # Metadata
    scanned_at = models.DateTimeField(auto_now_add=True)
    scanned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['scanned_at']
    
    def __str__(self):
        return f"{self.reference_type}: {self.value}"
