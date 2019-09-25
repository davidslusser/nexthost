from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_renderer_xlsx.mixins import XLSXFileMixin
from nexthost.api_mixins import AuditLogMixin

# import models
from hostmgr.models import (Owner,
                            Project,
                            Pattern,
                            AssetIdType,
                            Hostname
                            )

# import serializers
from hostmgr.serializers import (OwnerSerializer,
                                 ProjectSerializer,
                                 PatternSerializer,
                                 AssetIdTypeSerializer,
                                 HostnameSerializer
                                 )


class OwnerViewSet(XLSXFileMixin, AuditLogMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Owners to be viewed or edited.
    """
    lookup_field = "name"
    filter_backends = (DjangoFilterBackend, )
    model = Owner
    queryset = model.objects.all().select_related()
    serializer_class = OwnerSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "name", "group", "email", ]
    search_fields = filter_fields
    filename = 'owners.xlsx'

    @action(detail=True, methods=['get'])
    def projects(self, request, name=None):
        """ get the a list of all projects for this owner """
        self.filename = "{}_patterns.xlsx".format(self.model.__name__)
        try:
            data = self.get_object().get_projects()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = ProjectSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ProjectSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def patterns(self, request, name=None):
        """ get the a list of all patterns for this owner """
        self.filename = "{}_patterns.xlsx".format(self.model.__name__)
        try:
            data = self.get_object().get_patterns()
            page = self.paginate_queryset(data)
            if page is not None:
                serializer = PatternSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = PatternSerializer(data, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def hostnames(self, request, name=None):
        """ get the a list of all hostnames for this owner """
        self.filename = "{}_hostnames.xlsx".format(self.model.__name__)
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
    def available_hostnames(self, request, name=None):
        """ get the a list of all 'available' hostnames for this project """
        self.filename = "{}_available_hostnames.xlsx".format(self.model.__name__)
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
    def reserved_hostnames(self, request, name=None):
        """ get the a list of all 'reserved' hostnames for this project """
        self.filename = "{}_reserved_hostnames.xlsx".format(self.model.__name__)
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
    def assigned_hostnames(self, request, name=None):
        """ get the a list of all 'assigned' hostnames for this project """
        self.filename = "{}_assigned_hostnames.xlsx".format(self.model.__name__)
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
    def expired_hostnames(self, request, name=None):
        """ get the a list of all 'expired' hostnames for this project """
        self.filename = "{}_expired_hostnames.xlsx".format(self.model.name)
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


class ProjectViewSet(XLSXFileMixin, AuditLogMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Projects to be viewed or edited.
    """
    lookup_field = "name"
    filter_backends = (DjangoFilterBackend, )
    model = Project
    queryset = model.objects.all().select_related()
    serializer_class = ProjectSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "name", "owner", "description", ]
    search_fields = filter_fields
    filename = 'projects.xlsx'

    @action(detail=True, methods=['get'])
    def hostnames(self, request, name=None):
        """ get the a list of all hostnames for this project """
        try:
            self.filename = "{}_hostnames.xlsx".format(self.model.__name__)
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
    def available_hostnames(self, request, name=None):
        """ get the a list of all 'available' hostnames for this project """
        try:
            self.filename = "{}_available_hostnames.xlsx".format(self.model__name__)
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
    def reserved_hostnames(self, request, name=None):
        """ get the a list of all 'reserved' hostnames for this project """
        try:
            self.filename = "{}_reserved_hostnames.xlsx".format(self.model.__name__)
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
    def assigned_hostnames(self, request, name=None):
        """ get the a list of all 'assigned' hostnames for this project """
        try:
            self.filename = "{}_assigned_hostnames.xlsx".format(self.model.__name__)
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
    def expired_hostnames(self, request, name=None):
        """ get the a list of all 'expired' hostnames for this project """
        try:
            self.filename = "{}_expired_hostnames.xlsx".format(self.model.__name__)
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


class PatternViewSet(AuditLogMixin, XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Patterns to be viewed or edited.
    """
    lookup_field = "name"
    filter_backends = (DjangoFilterBackend, )
    model = Pattern
    queryset = model.objects.all().select_related()
    serializer_class = PatternSerializer
    filter_fields = ["id", "name", "description", "project", "prefix", "prefix_delimiter", "suffix", "suffix_delimiter",
                     "host_count", "increment", "start_from", "created_at", "updated_at"]
    search_fields = filter_fields
    filename = 'patterns.xlsx'

    @action(detail=True, methods=['get'])
    def hostnames(self, request, name=None):
        """ get the a list of all hostnames for this project """
        self.filename = "{}_hostnames.xlsx".format(self.model.__name__)
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
    def available_hostnames(self, request, name=None):
        """ get the a list of all 'available' hostnames for this project """
        self.filename = "{}_hostnames.xlsx".format(self.model.__name__)
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
    def reserved_hostnames(self, request, name=None):
        """ get the a list of all 'reserved' hostnames for this project """
        self.filename = "{}_hostnames.xlsx".format(self.model.__name__)
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
    def assigned_hostnames(self, request, name=None):
        """ get the a list of all 'assigned' hostnames for this project """
        self.filename = "{}_hostnames.xlsx".format(self.model.__name__)
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
    def expired_hostnames(self, request, name=None):
        """ get the a list of all 'expired' hostnames for this project """
        self.filename = "{}_hostnames.xlsx".format(self.model.__name__)
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

    # @action(detail=True, methods=['get'])
    # def get_next(self):
    #     """ get the next available hostname(s) for this pattern """
    #     try:
    #         print("HERE I AM!!!")
    #         data = json.loads(self.request.body)
    #         count = data.get('count', 1)
    #         consecutive = data.get('consecutive', None)
    #         pattern = self.get_object()
    #         return Response(json.dumps({"result": "it works!"}))
    #         # return Response(json.dumps({'hostnames': pattern.get_next_hostname(user=self.request.user,
    #         #                                                                    count=count,
    #         #                                                                    consecutive=consecutive)}))
    #     except Exception as err:
    #         return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)
    #
    # @action(detail=True, methods=['patch'])
    # def reserve_next(self):
    #     """ reserve the next available hostname(s) for this pattern """
    #     try:
    #         data = json.loads(self.request.body)
    #         count = data.get('count', 1)
    #         consecutive = data.get('consecutive', None)
    #         pattern = self.get_object()
    #         return Response(json.dumps({'hostnames': pattern.reserve_next_hostname(count=count,
    #                                                                                consecutive=consecutive)},
    #                                    status.HTTP_200_OK))
    #     except Exception as err:
    #         return Response({'messages': err}, status.HTTP_400_BAD_REQUEST)


class AssetIdTypeViewSet(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows AssetIdTypes to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = AssetIdType
    queryset = model.objects.all().select_related()
    serializer_class = AssetIdTypeSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "name", "description", ]
    search_fields = filter_fields


class HostnameViewSet(XLSXFileMixin, AuditLogMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Hostnames to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = Hostname
    queryset = model.objects.all().select_related()
    serializer_class = HostnameSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "pattern", "hostname", "asset_id", "asset_id_type",
                     "persistent", "status", "reservation_expires", "assignment_expires", ]
    search_fields = filter_fields
    filename = 'hostnames.xlsx'

    @action(detail=True, methods=['patch'])
    def assign(self):
        """ set a hostname to assigned; requires fields: asset_id, asset_id_type; optional fields: persistent"""
        print("TEST: trying to assign...")
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


    # extend assignment

    # extent reservation
