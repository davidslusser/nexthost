from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from handyhelpers.mixins.viewset_mixins import InvalidLookupMixin
from userextensions.mixins import ServiceAccountControlMixin
from drf_renderer_xlsx.mixins import XLSXFileMixin
from rest_flex_fields import is_expanded

# import models
from hostmgr.models import (Owner, Project, Pattern, AssetIdType, Hostname)

# import serializers
from hostmgr.serializers import (OwnerSerializer, ProjectSerializer, PatternSerializer,
                                 AssetIdTypeSerializer, HostnameSerializer)


# import filtersets
from hostmgr.filters import (OwnerFilter, ProjectFilter, PatternFilter, AssetIdTypeFilter, HostnameFilter)


class HostmgrBaseViewSet(InvalidLookupMixin, ServiceAccountControlMixin, XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, )


class OwnerViewSet(HostmgrBaseViewSet):
    """
    API endpoint that allows Owners to be viewed or edited.
    """
    model = Owner
    queryset = model.objects.all()
    serializer_class = OwnerSerializer
    filterset_fields = ['id', 'created_at', 'updated_at', 'active', 'name', 'group', 'email', ]
    lookup_field = 'name'

    @action(detail=True, methods=['get'])
    def stats(self, request, *args, **kwargs):
        """ get counts for related data (projects/patterns/hostnames) """
        try:
            owner = self.get_object()
            resp = {
                'name': owner.name,
                'project_count': owner.get_projects().count(),
                'pattern_count': owner.get_patterns().count(),
                'hostname_count': owner.get_hostnames().count(),
                'assigned_hostname_count': owner.get_assigned_hostnames().count(),
                'available_hostname_count': owner.get_available_hostnames().count(),
                'expired_hostname_count': owner.get_expired_hostnames().count(),
                'reserved_hostname_count': owner.get_reserved_hostnames().count(),
            }
            return Response(resp, status.HTTP_200_OK)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def projects(self, request, *args, **kwargs):
        """ get the a list of all projects for this owner """
        try:
            data = self.get_object().get_projects()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = ProjectSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ProjectSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'error': 'no data available for requested owner'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def patterns(self, request, *args, **kwargs):
        """ get the a list of all patterns for this owner """
        try:
            data = self.get_object().get_patterns()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = PatternSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = PatternSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'error': 'no data available for requested owner'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def hostnames(self, request, *args, **kwargs):
        """ get the a list of all hostnames for this owner """
        try:
            data = self.get_object().get_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': 'no data available for requested owner'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def available_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'available' hostnames for this project """
        try:
            data = self.get_object().get_available_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': 'no data available for requested owner'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def reserved_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'reserved' hostnames for this project """
        try:
            data = self.get_object().get_reserved_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': 'no data available for requested owner'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def assigned_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'assigned' hostnames for this project """
        try:
            data = self.get_object().get_assigned_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': 'no data available for requested owner'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def expired_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'expired' hostnames for this project """
        try:
            data = self.get_object().get_expired_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': 'no data available for requested owner'}, status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(HostmgrBaseViewSet):
    """
    API endpoint that allows Projects to be viewed or edited.
    """
    model = Project
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter
    lookup_field = 'name'

    def get_queryset(self):
        queryset = self.model.objects.all().select_related('owner')
        if is_expanded(self.request, 'owner'):
            queryset = queryset.select_related('owner__group')
        return queryset

    @action(detail=True, methods=['get'])
    def stats(self, request, *args, **kwargs):
        """ get counts for related data (patterns/hostnames) """
        try:
            project = self.get_object()
            resp = {
                'name': project.name,
                'pattern_count': project.get_pattern_count(),
                'hostname_count': project.get_hostname_count(),
                'assigned_hostname_count': project.get_assigned_hostname_count(),
                'available_hostname_count': project.get_available_hostname_count(),
                'expired_hostname_count': project.get_expired_hostname_count(),
                'reserved_hostname_count': project.get_reserved_hostname_count(),
            }
            return Response(resp, status.HTTP_200_OK)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def hostnames(self, request, *args, **kwargs):
        """ get the a list of all hostnames for this project """
        try:
            project = self.get_object()
            data = project.get_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def available_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'available' hostnames for this project """
        try:
            project = self.get_object()
            data = project.get_available_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def reserved_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'reserved' hostnames for this project """
        try:
            project = self.get_object()
            data = project.get_reserved_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def assigned_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'assigned' hostnames for this project """
        try:
            project = self.get_object()
            data = project.get_assigned_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def expired_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'expired' hostnames for this project """
        try:
            project = self.get_object()
            data = project.get_expired_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)


class PatternViewSet(HostmgrBaseViewSet):
    """
    API endpoint that allows Patterns to be viewed or edited.
    """
    model = Pattern
    queryset = model.objects.all().select_related()
    serializer_class = PatternSerializer
    filterset_class = PatternFilter
    lookup_field = 'name'

    @action(detail=True, methods=['get'])
    def stats(self, request, *args, **kwargs):
        """ get counts for related data (hostnames) """
        try:
            pattern = self.get_object()
            resp = {
                'hostname_count': pattern.get_hostnames().count(),
                'assigned_hostname_count': pattern.get_assigned_hostnames().count(),
                'available_hostname_count': pattern.get_available_hostnames().count(),
                'expired_hostname_count': pattern.get_expired_hostnames().count(),
                'reserved_hostname_count': pattern.get_reserved_hostnames().count(),
            }
            return Response(resp, status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def hostnames(self, request, *args, **kwargs):
        """ get the a list of all hostnames for this project """
        try:
            data = self.get_object().get_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def available_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'available' hostnames for this project """
        try:
            data = self.get_object().get_available_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def reserved_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'reserved' hostnames for this project """
        try:
            data = self.get_object().get_reserved_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def assigned_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'assigned' hostnames for this project """
        try:
            data = self.get_object().get_assigned_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def expired_hostnames(self, request, *args, **kwargs):
        """ get the a list of all 'expired' hostnames for this project """
        try:
            data = self.get_object().get_expired_hostnames()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = HostnameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HostnameSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)


class AssetIdTypeViewSet(HostmgrBaseViewSet):
    """
    API endpoint that allows AssetIdTypes to be viewed or edited.
    """
    model = AssetIdType
    queryset = model.objects.all().select_related()
    serializer_class = AssetIdTypeSerializer
    filterset_class = AssetIdTypeFilter
    lookup_field = 'name'


class HostnameViewSet(HostmgrBaseViewSet):
    """
    API endpoint that allows Hostnames to be viewed or edited.
    """
    model = Hostname
    serializer_class = HostnameSerializer
    filterset_class = HostnameFilter
    lookup_field = 'hostname'

    def get_queryset(self):
        queryset = self.model.objects.all().select_related('pattern', 'asset_id_type')
        if is_expanded(self.request, 'pattern'):
            queryset = queryset.select_related('pattern__project')
        return queryset

    @action(detail=True, methods=['patch'])
    def assign(self):
        """ set a hostname to assigned; requires fields: asset_id, asset_id_type; optional fields: persistent """
        try:
            hostname = self.get_object()
            hostname.assign_hostname(user=self.request.user)
            return Response(self.serializer_class.data, status.HTTP_200_OK)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def release(self):
        """ release the assignment on a hostname """
        try:
            hostname = self.get_object()
            hostname.release_hostname(user=self.request.user)
            return Response(self.serializer_class.data, status.HTTP_200_OK)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def reserve(self):
        """ set a hostname to status='reserved' """
        try:
            hostname = self.get_object()
            hostname.reserve_hostname(user=self.request.user)
            return Response(self.serializer_class.data, status.HTTP_200_OK)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)
