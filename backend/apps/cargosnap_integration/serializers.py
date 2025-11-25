from rest_framework import serializers
from .models import (
    CargoSnapFile, CargoSnapUpload, CargoSnapLocation,
    CargoSnapWorkflow, CargoSnapWorkflowStep, CargoSnapWorkflowRun,
    CargoSnapWorkflowRunStep, CargoSnapSyncLog
)


class CargoSnapUploadSerializer(serializers.ModelSerializer):
    # URLs completas para as imagens locais
    local_image_url = serializers.SerializerMethodField()
    local_thumb_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CargoSnapUpload
        fields = [
            'id', 'cargosnap_id', 'device_nick', 'upload_type',
            'created_at', 'scan_date_time', 'longitude', 'latitude',
            'geocoding_data', 'has_damage', 'damage_type_desc', 'comment',
            'workflow_description', 'workflow_step_description',
            'image_url', 'image_thumb', 'local_image_path', 'local_thumb_path',
            'local_image_url', 'local_thumb_url', 'image_downloaded'
        ]
    
    def get_local_image_url(self, obj):
        """Retorna URL completa da imagem local"""
        if obj.local_image_path and obj.image_downloaded:
            request = self.context.get('request')
            if request:
                from django.conf import settings
                return request.build_absolute_uri(f"{settings.MEDIA_URL}{obj.local_image_path}")
        return None
    
    def get_local_thumb_url(self, obj):
        """Retorna URL completa da thumbnail local"""
        if obj.local_thumb_path and obj.image_downloaded:
            request = self.context.get('request')
            if request:
                from django.conf import settings
                return request.build_absolute_uri(f"{settings.MEDIA_URL}{obj.local_thumb_path}")
        return None


class CargoSnapLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoSnapLocation
        fields = ['id', 'cargosnap_id', 'location']


class CargoSnapWorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoSnapWorkflowStep
        fields = [
            'id', 'cargosnap_id', 'order', 'description', 'step_type',
            'allow_skip', 'platform_description', 'data'
        ]


class CargoSnapWorkflowSerializer(serializers.ModelSerializer):
    steps = CargoSnapWorkflowStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = CargoSnapWorkflow
        fields = [
            'id', 'cargosnap_id', 'name', 'workflow_type', 'order',
            'created_at', 'updated_at', 'steps'
        ]


class CargoSnapWorkflowRunStepSerializer(serializers.ModelSerializer):
    workflow_step = CargoSnapWorkflowStepSerializer(read_only=True)
    
    class Meta:
        model = CargoSnapWorkflowRunStep
        fields = [
            'id', 'cargosnap_id', 'workflow_step', 'entity_type',
            'status', 'entity_ids', 'submit_date_time'
        ]


class CargoSnapWorkflowRunSerializer(serializers.ModelSerializer):
    workflow = CargoSnapWorkflowSerializer(read_only=True)
    run_steps = CargoSnapWorkflowRunStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = CargoSnapWorkflowRun
        fields = [
            'id', 'cargosnap_id', 'workflow', 'submit_date_time',
            'completed_at', 'run_steps'
        ]


class CargoSnapFileListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""
    
    class Meta:
        model = CargoSnapFile
        fields = [
            'id', 'cargosnap_id', 'scan_code', 'snap_count',
            'snap_count_with_damage', 'closed', 'created_at',
            'updated_at', 'sync_status'
        ]


class CargoSnapFileDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalhes"""
    
    uploads = CargoSnapUploadSerializer(many=True, read_only=True)
    locations = CargoSnapLocationSerializer(many=True, read_only=True)
    workflow_runs = CargoSnapWorkflowRunSerializer(many=True, read_only=True)
    
    # Contadores adicionais
    total_images = serializers.SerializerMethodField()
    downloaded_images = serializers.SerializerMethodField()
    images_with_damage = serializers.SerializerMethodField()
    
    class Meta:
        model = CargoSnapFile
        fields = [
            'id', 'cargosnap_id', 'scan_code', 'scan_code_format',
            'closed', 'created_at', 'updated_at', 'snap_count',
            'snap_count_with_damage', 'sync_status', 'last_synced_at',
            'uploads', 'locations', 'workflow_runs',
            'total_images', 'downloaded_images', 'images_with_damage'
        ]
    
    def get_total_images(self, obj):
        return obj.uploads.count()
    
    def get_downloaded_images(self, obj):
        return obj.uploads.filter(image_downloaded=True).count()
    
    def get_images_with_damage(self, obj):
        return obj.uploads.filter(has_damage=True).count()


class CargoSnapSyncLogSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = CargoSnapSyncLog
        fields = [
            'id', 'started_at', 'finished_at', 'status',
            'files_processed', 'files_created', 'files_updated', 'files_failed',
            'images_downloaded', 'images_failed', 'total_pages', 'current_page',
            'error_message', 'duration'
        ]
    
    def get_duration(self, obj):
        if obj.finished_at and obj.started_at:
            delta = obj.finished_at - obj.started_at
            return delta.total_seconds()
        return None


class CargoSnapStatsSerializer(serializers.Serializer):
    """Serializer para estatísticas gerais"""
    
    total_files = serializers.IntegerField()
    total_images = serializers.IntegerField()
    images_downloaded = serializers.IntegerField()
    images_pending = serializers.IntegerField()
    files_with_damage = serializers.IntegerField()
    total_damage_images = serializers.IntegerField()
    last_sync = serializers.DateTimeField(allow_null=True)
    sync_status = serializers.DictField()
