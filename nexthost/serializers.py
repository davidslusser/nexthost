from rest_framework import serializers
from auditlog.models import LogEntry
import json
from django.contrib.contenttypes.models import ContentType


class AuditLogSerializer(serializers.ModelSerializer):
    """
    Description:
        A custom (generic) AuditLog serializer. This serializer will remove changes in a LogEntry if the
        field_type_filter_list provided. By default, this includes entries of field types
        ReverseGenericManyToOneDescriptor and ReverseManyToOneDescriptor.

    Parameters:
        queryset               - queryset of LogEntry objects
        field_type_filter_list - list of field types to clean (remove) from LogEntry changes
    """

    def __init__(self, queryset=None, field_type_filter_list=None, *args, **kwargs):
        """ class entry point """
        super(AuditLogSerializer, self).__init__(*args, **kwargs)
        self.queryset = queryset
        self.instance_model = self.get_instance_model()
        if field_type_filter_list is None:
            self.field_type_filter_list = ['ReverseGenericManyToOneDescriptor', 'ReverseManyToOneDescriptor']
        else:
            self.field_type_filter_list = field_type_filter_list

    def get_instance_model(self):
        """ get the instance (parent) model by extracting and the content_type from the first log instance
        and looking up in ContentTYpe table """
        if self.queryset:
            return ContentType.objects.get(model=self.queryset[0].content_type).model_class()

    def get_field_type(self, field_name):
        """get the field type for a given field name in the instance model

        Args:
            field_name (str): Name of the attribute to look up

        Returns:
            str: Type of field, example: DeferredAttribute or ForwardManyToOneDescriptor or ReverseManyToOneDescriptor

        """
        # We are looping over "Changes" which in some cases might be for fields that no longer exist.
        # Example, we removed `snmp_public` but it still shows up in some older logs.  'fake' just makes this
        # function return 'str' if the field doesn't exist anymore.
        field_value = getattr(self.instance_model, field_name, 'fake')
        field_type = type(field_value).__name__
        return field_type

    @staticmethod
    def get_action(obj):
        """takes an instance of a auditlog "change" and returns the human-readable "action"

        Args:
            obj (LogEntry.change):

        Returns:
            str: 'create', 'update' or 'delete'
        """

        action_choices = {
            0: "create",
            1: "update",
            2: "delete",
        }
        return action_choices[obj.action]

    def get_changes(self, obj):
        """ remove changes from change fields that are of field types defined in self.field_type_filter) """
        if not self.field_type_filter_list:
            return obj.changes
        original_data = json.loads(obj.changes)
        cleaned_data = {k: v for k, v in original_data.items()
                        if self.get_field_type(k) not in self.field_type_filter_list}
        return json.dumps(cleaned_data)

    actor = serializers.StringRelatedField()
    action = serializers.SerializerMethodField(read_only=True, source='get_action')
    changes = serializers.SerializerMethodField(read_only=True, source='get_changes')

    class Meta:
        model = LogEntry
        fields = (
            'id',
            'action',
            'changes',
            'actor',
            'remote_addr',
            'timestamp',
            'additional_data',
        )
