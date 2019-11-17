from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin

# import models
from hostmgr.models import (Owner, Project, Pattern, AssetIdType, Hostname)


class OwnerSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = ["id", "created_at", "updated_at", "active", "name", "group", "email"]
        depth = 0


class HostnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostname
        fields = ["id", "created_at", "updated_at", "active", "pattern", "hostname", "asset_id", "asset_id_type",
                  "persistent", "status", "reservation_expires", "assignment_expires", ]
        depth = 0


class ProjectSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "created_at", "updated_at", "active", "name", "owner", "owner_id", "description"]
        depth = 0

    @staticmethod
    def get_owner_id(obj):
        return obj.owner.id


class PatternSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    project_id = serializers.SerializerMethodField()

    class Meta:
        model = Pattern
        fields = ["id", "name", "description", "project", "project_id", "prefix", "prefix_delimiter", "suffix",
                  "suffix_delimiter", "host_count", "increment", "start_from", "created_at", "updated_at",
                  ]
        depth = 0

    @staticmethod
    def get_project_id(obj):
        return obj.project.id


class AssetIdTypeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = AssetIdType
        fields = ["id", "created_at", "updated_at", "active", "name", "description", ]
        depth = 0
