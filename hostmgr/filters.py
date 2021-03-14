from rest_framework_filters.filters import RelatedFilter
from rest_framework_filters.filterset import FilterSet

"""
https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups
"""


# import models
from hostmgr.models import (Owner, Project, Pattern, AssetIdType, Hostname)


class OwnerFilter(FilterSet):
    class Meta:
        model = Owner
        fields = {
            'id': '__all__',
            'name': '__all__',
            'group': '__all__',
            'email': '__all__',
        }


class ProjectFilter(FilterSet):
    owner = RelatedFilter(OwnerFilter, field_name='owner', queryset=Owner.objects.all())

    class Meta:
        model = Project
        fields = {
            'id': '__all__',
            'name': '__all__',
            'description': '__all__',
        }


class PatternFilter(FilterSet):
    project = RelatedFilter(ProjectFilter, field_name='project', queryset=Project.objects.all().select_related('owner'))

    class Meta:
        model = Pattern
        fields = {
            'id': '__all__',
            'name': '__all__',
            'description': '__all__',
            'prefix': '__all__',
            'prefix_delimiter': '__all__',
            'suffix': '__all__',
            'suffix_delimiter': '__all__',
            'host_count': '__all__',
            'increment': '__all__',
            'start_from': '__all__',
        }


class AssetIdTypeFilter(FilterSet):
    class Meta:
        model = AssetIdType
        fields = {
            'id': '__all__',
            'name': '__all__',
            'description': '__all__',
        }


class HostnameFilter(FilterSet):
    asset_id_type = RelatedFilter(AssetIdTypeFilter, field_name='asset_id_type', queryset=AssetIdType.objects.all())
    pattern = RelatedFilter(PatternFilter, field_name='asset_id_type',
                            queryset=Pattern.objects.all().select_related('project'))

    class Meta:
        model = Hostname
        fields = {
            'id': '__all__',
            'hostname': '__all__',
            'host_number': '__all__',
            'asset_id': '__all__',
            'persistent': '__all__',
            'status': '__all__',
            'reservation_expires': '__all__',
            'assignment_expires': '__all__',
        }
