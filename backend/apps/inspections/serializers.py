"""
Serializers for Inspections app
"""
from rest_framework import serializers
from .models import (
    InspectionType, Inspection, InspectionPhoto, InspectionVideo,
    InspectionDocument, InspectionTag, InspectionTagRelation,
    InspectionSignature, InspectionComment, ScannedReference
)
from .structure_models import (
    ContainerStructure, DamageType, StructureInspectionItem,
    StructureInspectionPhoto, InspectionChecklist, ChecklistStructure
)


class InspectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionType
        fields = ['id', 'company', 'name', 'code', 'description', 'icon', 'color', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class InspectionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionPhoto
        fields = [
            'id', 'inspection', 'photo', 'thumbnail', 'title', 'description', 'caption',
            'taken_at', 'latitude', 'longitude', 'device_info', 'sequence_number', 
            'is_cover_photo', 'created_at'
        ]
        read_only_fields = ['taken_at', 'created_at']


class InspectionVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionVideo
        fields = [
            'id', 'inspection', 'video', 'thumbnail', 'title', 'description',
            'duration_seconds', 'file_size_mb', 'taken_at', 'created_at'
        ]
        read_only_fields = ['taken_at', 'created_at']


class InspectionDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    
    class Meta:
        model = InspectionDocument
        fields = [
            'id', 'inspection', 'document', 'document_type', 'title', 'description',
            'file_size_mb', 'uploaded_by', 'uploaded_by_name', 'created_at'
        ]
        read_only_fields = ['uploaded_by', 'created_at']


class InspectionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionTag
        fields = ['id', 'company', 'name', 'color', 'description', 'created_at']
        read_only_fields = ['created_at']


class InspectionSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionSignature
        fields = [
            'id', 'inspection', 'signature_type', 'signature_image', 'signer_name',
            'signer_email', 'signer_role', 'signed_at', 'ip_address', 'user_agent'
        ]
        read_only_fields = ['signed_at']


class InspectionCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_avatar = serializers.CharField(source='user.avatar', read_only=True)
    
    class Meta:
        model = InspectionComment
        fields = [
            'id', 'inspection', 'user', 'user_name', 'user_avatar', 'comment',
            'is_internal', 'parent_comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class ScannedReferenceSerializer(serializers.ModelSerializer):
    scanned_by_name = serializers.CharField(source='scanned_by.full_name', read_only=True)
    
    class Meta:
        model = ScannedReference
        fields = [
            'id', 'inspection', 'reference_type', 'value', 'raw_data',
            'is_valid', 'validation_message', 'scanned_at', 'scanned_by', 'scanned_by_name'
        ]
        read_only_fields = ['scanned_at', 'scanned_by']


class InspectionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    inspection_type_name = serializers.CharField(source='inspection_type.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    inspector_name = serializers.CharField(source='inspector.full_name', read_only=True)
    photo_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Inspection
        fields = [
            'id', 'company', 'company_name', 'inspection_type', 'inspection_type_name',
            'reference_number', 'external_reference', 'title', 'status',
            'assigned_to', 'assigned_to_name', 'inspector', 'inspector_name',
            'location', 'scheduled_date', 'started_at', 'completed_at',
            'customer_name', 'container_number', 'seal_number', 'vehicle_plate',
            'photo_count', 'created_at'
        ]
        read_only_fields = ['reference_number', 'created_at']
    
    def get_photo_count(self, obj):
        return obj.photos.count()


class InspectionDetailSerializer(serializers.ModelSerializer):
    """Complete serializer for detail views"""
    company_name = serializers.CharField(source='company.name', read_only=True)
    inspection_type_name = serializers.CharField(source='inspection_type.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    inspector_name = serializers.CharField(source='inspector.full_name', read_only=True)
    
    photos = InspectionPhotoSerializer(many=True, read_only=True)
    videos = InspectionVideoSerializer(many=True, read_only=True)
    documents = InspectionDocumentSerializer(many=True, read_only=True)
    signatures = InspectionSignatureSerializer(many=True, read_only=True)
    comments = InspectionCommentSerializer(many=True, read_only=True)
    scanned_references = ScannedReferenceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Inspection
        fields = [
            'id', 'company', 'company_name', 'inspection_type', 'inspection_type_name',
            'reference_number', 'external_reference', 'title', 'description', 'status',
            'assigned_to', 'assigned_to_name', 'inspector', 'inspector_name',
            'location', 'latitude', 'longitude', 'weather_condition', 'temperature',
            'scheduled_date', 'started_at', 'completed_at',
            'customer_name', 'customer_email', 'customer_phone',
            'container_number', 'seal_number', 'booking_number', 'vessel_name', 'voyage_number',
            'container_type', 'container_size', 'cargo_description', 'cargo_weight',
            'vehicle_plate', 'vehicle_model', 'vehicle_year', 'vehicle_vin',
            'custom_fields', 'metadata',
            'photos', 'videos', 'documents', 'signatures', 'comments', 'scanned_references',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['reference_number', 'created_at', 'updated_at']


class InspectionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating inspections"""
    
    # Make company optional in input since it's auto-added from request.user
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Inspection
        fields = [
            'id', 'company', 'inspection_type', 'external_reference', 'title', 'description',
            'status', 'assigned_to', 'inspector', 'location', 'latitude', 'longitude',
            'weather_condition', 'temperature', 'scheduled_date', 'started_at', 'completed_at',
            'customer_name', 'customer_email', 'customer_phone',
            'container_number', 'seal_number', 'booking_number', 'vessel_name', 'voyage_number',
            'container_type', 'container_size', 'cargo_description', 'cargo_weight',
            'vehicle_plate', 'vehicle_model', 'vehicle_year', 'vehicle_vin',
            'custom_fields', 'metadata'
        ]
        read_only_fields = ['id', 'company']


# Structure and Damage Serializers

class ContainerStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerStructure
        fields = [
            'id', 'company', 'code', 'name', 'description', 'group',
            'is_critical', 'requires_photo', 'is_active', 'sequence', 'created_at'
        ]
        read_only_fields = ['created_at']


class DamageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DamageType
        fields = [
            'id', 'company', 'code', 'name', 'description', 'default_severity',
            'affects_operation', 'requires_repair', 'requires_photo', 
            'requires_measurement', 'is_active', 'color', 'sequence', 'created_at'
        ]
        read_only_fields = ['created_at']


class StructureInspectionItemSerializer(serializers.ModelSerializer):
    structure_name = serializers.CharField(source='structure.name', read_only=True)
    structure_code = serializers.CharField(source='structure.code', read_only=True)
    damage_type_name = serializers.CharField(source='damage_type.name', read_only=True)
    inspected_by_name = serializers.CharField(source='inspected_by.full_name', read_only=True)
    
    class Meta:
        model = StructureInspectionItem
        fields = [
            'id', 'inspection', 'structure', 'structure_name', 'structure_code',
            'status', 'damage_type', 'damage_type_name', 'notes',
            'measurement_length', 'measurement_width', 'measurement_depth',
            'location_description', 'has_photo', 'photo_count',
            'inspected_by', 'inspected_by_name', 'inspected_at',
            'severity_override', 'final_severity', 'created_at'
        ]
        read_only_fields = ['inspected_by', 'inspected_at', 'final_severity', 'created_at']


class ChecklistStructureSerializer(serializers.ModelSerializer):
    structure = ContainerStructureSerializer(read_only=True)
    structure_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ChecklistStructure
        fields = ['id', 'structure', 'structure_id', 'sequence', 'is_required', 'notes']


class InspectionChecklistSerializer(serializers.ModelSerializer):
    structures_detail = ChecklistStructureSerializer(source='checkliststructure_set', many=True, read_only=True)
    structure_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = InspectionChecklist
        fields = [
            'id', 'company', 'name', 'description', 'container_type',
            'is_active', 'is_default', 'usage_count',
            'structures_detail', 'structure_count',
            'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['usage_count', 'created_by', 'created_at']
    
    def get_structure_count(self, obj):
        return obj.structures.count()
