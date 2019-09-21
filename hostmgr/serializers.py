from rest_framework import serializers
# import models
from hostmgr.models import (Owner,
                            Project,
                            Pattern,
                            AssetIdType,
                            Hostname
                            )


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ["id", "created_at", "updated_at", "active", "name", "group", "email", ]
        depth = 0


class HostnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostname
        fields = ["id", "created_at", "updated_at", "active", "pattern", "hostname", "asset_id", "asset_id_type",
                  "persistent", "status", "reservation_expires", "assignment_expires", ]
        depth = 0


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "created_at", "updated_at", "active", "name", "owner", "description", ]
        depth = 0


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        # myfield = serializers.SerializerMethodField(read_only=True, source='myfield')

        fields = ["id", "name", "description", "project", "prefix", "prefix_delimiter", "suffix", "suffix_delimiter",
                  "host_count", "increment", "start_from", "created_at", "updated_at", "myfield"]
        # read_only_fields = ["myfield"]
        depth = 0


class AssetIdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetIdType
        fields = ["id", "created_at", "updated_at", "active", "name", "description", ]
        depth = 0
