from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CargoSnapFile, CargoSnapUpload, CargoSnapLocation,
    CargoSnapWorkflow, CargoSnapWorkflowStep, CargoSnapWorkflowRun,
    CargoSnapWorkflowRunStep, CargoSnapFormSubmit, CargoSnapField,
    CargoSnapSyncLog
)


@admin.register(CargoSnapFile)
class CargoSnapFileAdmin(admin.ModelAdmin):
    list_display = ['cargosnap_id', 'scan_code', 'snap_count', 'snap_count_with_damage', 
                    'closed', 'sync_status', 'created_at', 'last_synced_at']
    list_filter = ['sync_status', 'closed', 'created_at']
    search_fields = ['scan_code', 'cargosnap_id']
    readonly_fields = ['last_synced_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('cargosnap_id', 'scan_code', 'scan_code_format', 'closed')
        }),
        ('Estatísticas', {
            'fields': ('snap_count', 'snap_count_with_damage', 'recent_snap_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_synced_at')
        }),
        ('Sincronização', {
            'fields': ('sync_status', 'sync_error')
        }),
    )


class CargoSnapUploadInline(admin.TabularInline):
    model = CargoSnapUpload
    extra = 0
    fields = ['cargosnap_id', 'device_nick', 'scan_date_time', 'has_damage', 
              'workflow_step_description', 'image_downloaded', 'thumbnail_preview']
    readonly_fields = ['thumbnail_preview']
    
    def thumbnail_preview(self, obj):
        if obj.image_thumb:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image_thumb)
        return "-"
    thumbnail_preview.short_description = 'Preview'


@admin.register(CargoSnapUpload)
class CargoSnapUploadAdmin(admin.ModelAdmin):
    list_display = ['cargosnap_id', 'file', 'device_nick', 'scan_date_time', 
                    'has_damage', 'workflow_step_description', 'image_downloaded', 'thumbnail_preview']
    list_filter = ['has_damage', 'image_downloaded', 'upload_type', 'scan_date_time']
    search_fields = ['cargosnap_id', 'file__scan_code', 'device_nick']
    ordering = ['-scan_date_time']
    readonly_fields = ['thumbnail_preview', 'full_image_preview']
    
    fieldsets = (
        ('Upload', {
            'fields': ('file', 'cargosnap_id', 'upload_type', 'scan_date_time', 'created_at')
        }),
        ('Dispositivo', {
            'fields': ('tenant_id', 'device_id', 'device_nick')
        }),
        ('Localização', {
            'fields': ('latitude', 'longitude', 'geocoding_data')
        }),
        ('Danos', {
            'fields': ('has_damage', 'damage_type_id', 'damage_type_desc', 'comment')
        }),
        ('Workflow', {
            'fields': ('workflow_id', 'workflow_step_id', 'workflow_description', 
                      'workflow_step_description')
        }),
        ('Imagens', {
            'fields': ('image_path', 'image_url', 'image_thumb', 
                      'local_image_path', 'local_thumb_path', 'image_downloaded',
                      'thumbnail_preview', 'full_image_preview')
        }),
    )
    
    def thumbnail_preview(self, obj):
        if obj.image_thumb:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image_thumb)
        return "-"
    thumbnail_preview.short_description = 'Thumbnail'
    
    def full_image_preview(self, obj):
        if obj.image_url:
            return format_html('<a href="{}" target="_blank"><img src="{}" style="max-width: 400px;"/></a>', 
                             obj.image_url, obj.image_url)
        return "-"
    full_image_preview.short_description = 'Imagem Completa'


@admin.register(CargoSnapLocation)
class CargoSnapLocationAdmin(admin.ModelAdmin):
    list_display = ['file', 'location', 'cargosnap_id']
    search_fields = ['file__scan_code', 'location']


@admin.register(CargoSnapWorkflow)
class CargoSnapWorkflowAdmin(admin.ModelAdmin):
    list_display = ['cargosnap_id', 'name', 'workflow_type', 'order', 'created_at']
    list_filter = ['workflow_type', 'force', 'close_file_after_completion']
    search_fields = ['name', 'cargosnap_id']
    ordering = ['order', 'name']


@admin.register(CargoSnapWorkflowStep)
class CargoSnapWorkflowStepAdmin(admin.ModelAdmin):
    list_display = ['cargosnap_id', 'workflow', 'order', 'description', 'step_type', 'allow_skip']
    list_filter = ['step_type', 'allow_skip', 'workflow']
    search_fields = ['description', 'cargosnap_id']
    ordering = ['workflow', 'order']


@admin.register(CargoSnapWorkflowRun)
class CargoSnapWorkflowRunAdmin(admin.ModelAdmin):
    list_display = ['cargosnap_id', 'file', 'workflow', 'submit_date_time', 'completed_at']
    list_filter = ['workflow', 'submit_date_time']
    search_fields = ['file__scan_code', 'workflow__name', 'client_key']
    ordering = ['-submit_date_time']


@admin.register(CargoSnapWorkflowRunStep)
class CargoSnapWorkflowRunStepAdmin(admin.ModelAdmin):
    list_display = ['cargosnap_id', 'workflow_run', 'workflow_step', 'status', 'submit_date_time']
    list_filter = ['status', 'entity_type']
    search_fields = ['workflow_run__file__scan_code', 'workflow_step__description']
    ordering = ['workflow_run', 'submit_date_time']


@admin.register(CargoSnapFormSubmit)
class CargoSnapFormSubmitAdmin(admin.ModelAdmin):
    list_display = ['cargosnap_id', 'file', 'created_at']
    search_fields = ['file__scan_code', 'cargosnap_id']
    ordering = ['-created_at']


@admin.register(CargoSnapField)
class CargoSnapFieldAdmin(admin.ModelAdmin):
    list_display = ['file', 'field_name', 'field_value']
    search_fields = ['file__scan_code', 'field_name', 'field_value']


@admin.register(CargoSnapSyncLog)
class CargoSnapSyncLogAdmin(admin.ModelAdmin):
    list_display = ['started_at', 'finished_at', 'status', 'files_processed', 
                    'files_created', 'files_updated', 'images_downloaded']
    list_filter = ['status', 'started_at']
    readonly_fields = ['started_at', 'finished_at', 'files_processed', 'files_created', 
                      'files_updated', 'files_failed', 'images_downloaded', 'images_failed']
    ordering = ['-started_at']
    
    fieldsets = (
        ('Período', {
            'fields': ('started_at', 'finished_at', 'status')
        }),
        ('Arquivos', {
            'fields': ('files_processed', 'files_created', 'files_updated', 'files_failed')
        }),
        ('Imagens', {
            'fields': ('images_downloaded', 'images_failed')
        }),
        ('Paginação', {
            'fields': ('total_pages', 'current_page')
        }),
        ('Detalhes', {
            'fields': ('error_message', 'details')
        }),
    )
