from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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


class OwnerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Owners to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = Owner
    queryset = model.objects.all().select_related()
    serializer_class = OwnerSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "name", "group", "email", ]
    search_fields = filter_fields


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Projects to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = Project
    queryset = model.objects.all().select_related()
    serializer_class = ProjectSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "name", "owner", "description", ]
    search_fields = filter_fields


class PatternViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Patterns to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = Pattern
    queryset = model.objects.all().select_related()
    serializer_class = PatternSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "name", "description", "project", "prefix",
                     "delimiter", "host_count", "increment", "start_from", ]
    search_fields = filter_fields


class AssetIdTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows AssetIdTypes to be viewed or edited.
    """
    filter_backends = (DjangoFilterBackend, )
    model = AssetIdType
    queryset = model.objects.all().select_related()
    serializer_class = AssetIdTypeSerializer
    filter_fields = ["id", "created_at", "updated_at", "active", "name", "description", ]
    search_fields = filter_fields


class HostnameViewSet(viewsets.ReadOnlyModelViewSet):
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

    @action(detail=True, methods=['patch'])
    def assign(self):
        """ set a hostname to assigned """
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
