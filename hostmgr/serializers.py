from rest_framework import serializers
# import models
from hostmgr.models import (Owner,
                            Project,
                            Pattern,
                            AssetIdType,
                            Hostname
                            )


class OwnerSerializer(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()
    pattern_count = serializers.SerializerMethodField()
    hostname_count = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = ["id", "created_at", "updated_at", "active", "name", "group", "email",
                  "project_count", "pattern_count", "hostname_count"]
        depth = 0

    @staticmethod
    def get_project_count(obj):
        return obj.get_projects().count()

    @staticmethod
    def get_pattern_count(obj):
        return obj.get_patterns().count()

    @staticmethod
    def get_hostname_count(obj):
        return obj.get_hostnames().count()


class HostnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostname
        fields = ["id", "created_at", "updated_at", "active", "pattern", "hostname", "asset_id", "asset_id_type",
                  "persistent", "status", "reservation_expires", "assignment_expires", ]
        depth = 0


class ProjectSerializer(serializers.ModelSerializer):
    pattern_count = serializers.SerializerMethodField()
    hostname_count = serializers.SerializerMethodField()
    available_hostname_count = serializers.SerializerMethodField()
    assigned_hostname_count = serializers.SerializerMethodField()
    reserved_hostname_count = serializers.SerializerMethodField()
    expired_hostname_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "created_at", "updated_at", "active", "name", "owner", "description", "pattern_count",
                  "hostname_count", "available_hostname_count", "assigned_hostname_count",
                  "reserved_hostname_count", "expired_hostname_count"]
        depth = 0

    @staticmethod
    def get_pattern_count(obj):
        return obj.get_patterns().count()

    @staticmethod
    def get_hostname_count(obj):
        return obj.get_hostnames().count()

    @staticmethod
    def get_available_hostname_count(obj):
        return obj.get_available_hostnames().count()

    @staticmethod
    def get_assigned_hostname_count(obj):
        return obj.get_assigned_hostnames().count()

    @staticmethod
    def get_reserved_hostname_count(obj):
        return obj.get_reserved_hostnames().count()

    @staticmethod
    def get_expired_hostname_count(obj):
        return obj.get_expired_hostnames().count()


class PatternSerializer(serializers.ModelSerializer):
    hostname_count = serializers.SerializerMethodField()
    available_hostname_count = serializers.SerializerMethodField()
    assigned_hostname_count = serializers.SerializerMethodField()
    reserved_hostname_count = serializers.SerializerMethodField()
    expired_hostname_count = serializers.SerializerMethodField()

    class Meta:
        model = Pattern
        fields = ["id", "name", "description", "project", "prefix", "prefix_delimiter", "suffix", "suffix_delimiter",
                  "host_count", "increment", "start_from", "created_at", "updated_at", "hostname_count",
                  "available_hostname_count", "assigned_hostname_count",
                  "reserved_hostname_count", "expired_hostname_count",
                  ]
        depth = 0

    @staticmethod
    def get_hostname_count(obj):
        return obj.get_hostnames().count()

    @staticmethod
    def get_available_hostname_count(obj):
        return obj.get_available_hostnames().count()

    @staticmethod
    def get_assigned_hostname_count(obj):
        return obj.get_assigned_hostnames().count()

    @staticmethod
    def get_reserved_hostname_count(obj):
        return obj.get_reserved_hostnames().count()

    @staticmethod
    def get_expired_hostname_count(obj):
        return obj.get_expired_hostnames().count()


class AssetIdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetIdType
        fields = ["id", "created_at", "updated_at", "active", "name", "description", ]
        depth = 0
