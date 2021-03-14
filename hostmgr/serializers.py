from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

# import models
from hostmgr.models import (Owner, Project, Pattern, AssetIdType, Hostname)


class OwnerSerializer(FlexFieldsModelSerializer):
    group = serializers.StringRelatedField()

    class Meta:
        model = Owner
        fields = ['id', 'created_at', 'updated_at', 'active', 'name', 'group', 'email']


class ProjectSerializer(FlexFieldsModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ['id', 'created_at', 'updated_at', 'active', 'name', 'description', 'owner']
        expandable_fields = {
            'owner': OwnerSerializer,
        }


class PatternSerializer(FlexFieldsModelSerializer):
    project = serializers.StringRelatedField()

    class Meta:
        model = Pattern
        fields = ['id', 'name', 'description', 'project', 'project_id', 'prefix', 'prefix_delimiter', 'suffix',
                  'suffix_delimiter', 'host_count', 'increment', 'start_from', 'created_at', 'updated_at',
                  ]
        expandable_fields = {
            'project': ProjectSerializer,
        }


class AssetIdTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = AssetIdType
        fields = ['id', 'created_at', 'updated_at', 'active', 'name', 'description', ]
        depth = 0


class HostnameSerializer(FlexFieldsModelSerializer):
    pattern = serializers.StringRelatedField()
    asset_id_type = serializers.StringRelatedField()

    class Meta:
        model = Hostname
        fields = ['id', 'created_at', 'updated_at', 'active', 'pattern', 'hostname', 'asset_id', 'asset_id_type',
                  'persistent', 'status', 'reservation_expires', 'assignment_expires', ]
        expandable_fields = {
            'pattern': PatternSerializer,
            'asset_id_type': AssetIdTypeSerializer,
        }
