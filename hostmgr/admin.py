from django.contrib import admin

# import models
from hostmgr.models import (Owner,
                            Project,
                            Pattern,
                            AssetIdType,
                            Hostname
                            )


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'group', 'email']
    search_fields = ['name', 'email']
    list_filter = ['active', 'group']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'owner', 'description']
    search_fields = ['name', 'description']
    list_filter = ['active', 'owner']


class PatternAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'description', 'project', 'prefix', 'delimiter', 'host_count', 'increment', 'start_from']
    search_fields = ['name', 'description', 'prefix', 'delimiter', 'host_count', 'increment', 'start_from']
    list_filter = ['active', 'project']


class AssetIdTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['active']


class HostnameAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'active', 'pattern', 'hostname', 'asset_id', 'asset_id_type', 'persistent', 'status', 'reservation_expires', 'assignment_expires']
    search_fields = ['hostname', 'asset_id', 'status']
    list_filter = ['active', 'pattern', 'asset_id_type', 'persistent', 'status']


# register models
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Pattern, PatternAdmin)
admin.site.register(AssetIdType, AssetIdTypeAdmin)
admin.site.register(Hostname, HostnameAdmin)
