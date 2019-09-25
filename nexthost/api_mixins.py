from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from nexthost.serializers import AuditLogSerializer


class AuditLogMixin(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ API mixin to get audit log entries attached to an object """
    # field_type_filter_list defines list of field types to remove from LogEntry changes
    field_type_filter_list = None
    # filename is used for export like renderers such as XLSXFileMixin
    filename = None

    @action(detail=True, methods=['get'])
    def logs(self, request, name=None):
        self.filename = "{}_logs.xlsx".format(self.get_object())
        if getattr(self.get_object(), 'logentry_set', None):
            queryset = self.get_object().logentry_set.all().order_by('-timestamp')
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(
                    AuditLogSerializer(page,
                                       field_type_filter_list=self.field_type_filter_list,
                                       many=True,
                                       read_only=True).data
                )
        else:
            queryset = None
        return Response(
            AuditLogSerializer(queryset,
                               field_type_filter_list=self.field_type_filter_list,
                               many=True,
                               read_only=True).data
        )
