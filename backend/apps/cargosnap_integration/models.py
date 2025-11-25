from django.db import models
from django.contrib.postgres.fields import ArrayField
import json


class CargoSnapFile(models.Model):
    """Arquivo principal do CargoSnap (container/unidade)"""
    
    # Dados principais do arquivo
    cargosnap_id = models.BigIntegerField(unique=True, db_index=True)
    scan_code = models.CharField(max_length=100, db_index=True, help_text="Código do container")
    scan_code_format = models.CharField(max_length=50, blank=True, null=True)
    closed = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    # Metadados
    recent_snap_id = models.BigIntegerField(blank=True, null=True)
    snap_count = models.IntegerField(default=0)
    snap_count_with_damage = models.IntegerField(default=0)
    
    # Controle de sincronização
    last_synced_at = models.DateTimeField(auto_now=True)
    sync_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendente'),
            ('syncing', 'Sincronizando'),
            ('completed', 'Completo'),
            ('error', 'Erro')
        ],
        default='pending'
    )
    sync_error = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'cargosnap_files'
        verbose_name = 'Arquivo CargoSnap'
        verbose_name_plural = 'Arquivos CargoSnap'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['scan_code', '-created_at']),
            models.Index(fields=['sync_status']),
        ]
    
    def __str__(self):
        return f"{self.scan_code} (ID: {self.cargosnap_id})"


class CargoSnapUpload(models.Model):
    """Fotos/imagens capturadas no CargoSnap"""
    
    file = models.ForeignKey(
        CargoSnapFile,
        on_delete=models.CASCADE,
        related_name='uploads'
    )
    
    # Dados principais do upload
    cargosnap_id = models.BigIntegerField(unique=True, db_index=True)
    tenant_id = models.IntegerField()
    device_id = models.IntegerField()
    device_nick = models.CharField(max_length=200, blank=True, null=True)
    upload_type = models.CharField(max_length=50)
    
    # Timestamps
    created_at = models.DateTimeField()
    scan_date_time = models.DateTimeField()
    
    # Localização
    longitude = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    geocoding_data = models.JSONField(blank=True, null=True, help_text="Dados completos de geocoding")
    
    # Danos
    has_damage = models.BooleanField(default=False)
    damage_type_id = models.IntegerField(blank=True, null=True)
    damage_type_desc = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    
    # Tipo de documento
    document_type_id = models.IntegerField(blank=True, null=True)
    document_type_desc = models.CharField(max_length=200, blank=True, null=True)
    
    # Workflow
    workflow_id = models.IntegerField(blank=True, null=True)
    workflow_step_id = models.IntegerField(blank=True, null=True)
    workflow_description = models.CharField(max_length=500, blank=True, null=True)
    workflow_step_description = models.CharField(max_length=500, blank=True, null=True)
    
    # Imagens
    image_path = models.CharField(max_length=500)
    image_url = models.URLField(max_length=1000)
    image_thumb = models.URLField(max_length=1000)
    
    # Arquivos locais
    local_image_path = models.CharField(max_length=500, blank=True, null=True, help_text="Caminho da imagem baixada localmente")
    local_thumb_path = models.CharField(max_length=500, blank=True, null=True, help_text="Caminho da thumbnail baixada localmente")
    image_downloaded = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'cargosnap_uploads'
        verbose_name = 'Upload CargoSnap'
        verbose_name_plural = 'Uploads CargoSnap'
        ordering = ['scan_date_time']
        indexes = [
            models.Index(fields=['file', 'scan_date_time']),
            models.Index(fields=['workflow_id']),
            models.Index(fields=['has_damage']),
            models.Index(fields=['image_downloaded']),
        ]
    
    def __str__(self):
        return f"Upload {self.cargosnap_id} - {self.file.scan_code}"


class CargoSnapLocation(models.Model):
    """Localizações dos arquivos"""
    
    file = models.ForeignKey(
        CargoSnapFile,
        on_delete=models.CASCADE,
        related_name='locations'
    )
    
    cargosnap_id = models.IntegerField()
    location = models.CharField(max_length=500)
    
    class Meta:
        db_table = 'cargosnap_locations'
        verbose_name = 'Localização CargoSnap'
        verbose_name_plural = 'Localizações CargoSnap'
        unique_together = [['file', 'cargosnap_id']]
    
    def __str__(self):
        return f"{self.location} - {self.file.scan_code}"


class CargoSnapWorkflow(models.Model):
    """Workflows do CargoSnap"""
    
    cargosnap_id = models.IntegerField(unique=True, db_index=True)
    tenant_id = models.IntegerField()
    name = models.CharField(max_length=500)
    workflow_type = models.CharField(max_length=50)
    force = models.BooleanField(default=False)
    
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    language = models.CharField(max_length=10, blank=True, null=True)
    location_filter = models.CharField(max_length=200, blank=True, null=True)
    close_file_after_completion = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    clear_app_after_completion = models.BooleanField(default=False)
    info_url = models.URLField(max_length=1000, blank=True, null=True)
    
    class Meta:
        db_table = 'cargosnap_workflows'
        verbose_name = 'Workflow CargoSnap'
        verbose_name_plural = 'Workflows CargoSnap'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} (ID: {self.cargosnap_id})"


class CargoSnapWorkflowStep(models.Model):
    """Etapas dos workflows"""
    
    workflow = models.ForeignKey(
        CargoSnapWorkflow,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    
    cargosnap_id = models.IntegerField(unique=True, db_index=True)
    tenant_id = models.IntegerField()
    order = models.IntegerField()
    description = models.CharField(max_length=500)
    step_type = models.CharField(max_length=50)
    allow_skip = models.BooleanField(default=False)
    platform_description = models.CharField(max_length=500, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    info_url = models.URLField(max_length=1000, blank=True, null=True)
    
    class Meta:
        db_table = 'cargosnap_workflow_steps'
        verbose_name = 'Etapa de Workflow'
        verbose_name_plural = 'Etapas de Workflow'
        ordering = ['workflow', 'order']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.description}"


class CargoSnapWorkflowRun(models.Model):
    """Execuções de workflows"""
    
    file = models.ForeignKey(
        CargoSnapFile,
        on_delete=models.CASCADE,
        related_name='workflow_runs'
    )
    workflow = models.ForeignKey(
        CargoSnapWorkflow,
        on_delete=models.CASCADE,
        related_name='runs'
    )
    
    cargosnap_id = models.IntegerField(unique=True, db_index=True)
    client_key = models.CharField(max_length=50)
    tenant_id = models.IntegerField()
    
    submit_date_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    started_on_device_at = models.DateTimeField(blank=True, null=True)
    finished_on_device_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'cargosnap_workflow_runs'
        verbose_name = 'Execução de Workflow'
        verbose_name_plural = 'Execuções de Workflow'
        ordering = ['-submit_date_time']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.file.scan_code}"


class CargoSnapWorkflowRunStep(models.Model):
    """Etapas executadas em uma workflow run"""
    
    workflow_run = models.ForeignKey(
        CargoSnapWorkflowRun,
        on_delete=models.CASCADE,
        related_name='run_steps'
    )
    workflow_step = models.ForeignKey(
        CargoSnapWorkflowStep,
        on_delete=models.CASCADE,
        related_name='executions'
    )
    
    cargosnap_id = models.IntegerField(unique=True, db_index=True)
    entity_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    entity_ids = models.JSONField(help_text="Array de IDs das entidades relacionadas")
    device_id = models.IntegerField()
    tenant_id = models.IntegerField()
    
    submit_date_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'cargosnap_workflow_run_steps'
        verbose_name = 'Etapa Executada'
        verbose_name_plural = 'Etapas Executadas'
        ordering = ['workflow_run', 'submit_date_time']
    
    def __str__(self):
        return f"{self.workflow_run} - {self.workflow_step.description}"


class CargoSnapFormSubmit(models.Model):
    """Formulários submetidos no CargoSnap"""
    
    file = models.ForeignKey(
        CargoSnapFile,
        on_delete=models.CASCADE,
        related_name='form_submits'
    )
    
    cargosnap_id = models.IntegerField(unique=True, db_index=True)
    form_data = models.JSONField(help_text="Dados completos do formulário")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cargosnap_form_submits'
        verbose_name = 'Formulário Submetido'
        verbose_name_plural = 'Formulários Submetidos'
    
    def __str__(self):
        return f"Form {self.cargosnap_id} - {self.file.scan_code}"


class CargoSnapField(models.Model):
    """Campos customizados dos arquivos"""
    
    file = models.ForeignKey(
        CargoSnapFile,
        on_delete=models.CASCADE,
        related_name='fields'
    )
    
    field_name = models.CharField(max_length=200)
    field_value = models.TextField()
    field_data = models.JSONField(blank=True, null=True, help_text="Dados completos do campo")
    
    class Meta:
        db_table = 'cargosnap_fields'
        verbose_name = 'Campo CargoSnap'
        verbose_name_plural = 'Campos CargoSnap'
    
    def __str__(self):
        return f"{self.field_name}: {self.field_value}"


class CargoSnapSyncLog(models.Model):
    """Log de sincronizações"""
    
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('running', 'Executando'),
            ('completed', 'Completo'),
            ('error', 'Erro'),
            ('partial', 'Parcial')
        ],
        default='running'
    )
    
    files_processed = models.IntegerField(default=0)
    files_created = models.IntegerField(default=0)
    files_updated = models.IntegerField(default=0)
    files_failed = models.IntegerField(default=0)
    
    images_downloaded = models.IntegerField(default=0)
    images_failed = models.IntegerField(default=0)
    
    total_pages = models.IntegerField(default=0)
    current_page = models.IntegerField(default=0)
    
    error_message = models.TextField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    
    class Meta:
        db_table = 'cargosnap_sync_logs'
        verbose_name = 'Log de Sincronização'
        verbose_name_plural = 'Logs de Sincronização'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Sync {self.started_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.status}"
