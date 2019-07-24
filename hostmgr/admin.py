from django.contrib import admin

# import models
from hostmgr.models import (Owner,
                            Project,
                            HostnamePattern,
                            AssetIdType,
                            Hostname
                            )


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'is_active', 'name', 'group', 'email']
    search_fields = ['name', 'email']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'is_active', 'name', 'owner', 'description']
    search_fields = ['name', 'description']


class HostnamePatternAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'is_active', 'name', 'description', 'project', 'prefix', 'delimiter', 'max_hosts', 'increment', 'start_from']
    search_fields = ['name', 'description', 'prefix', 'delimiter', 'max_hosts', 'increment', 'start_from']


class AssetIdTypeAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'is_active', 'name', 'description']
    search_fields = ['name', 'description']


class HostnameAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'is_active', 'hostname', 'asset_id', 'asset_id_type', 'is_assigned', 'is_eternal', 'is_reserved', 'reservation_expires', 'assignment_expires']
    search_fields = ['hostname', 'asset_id']


# register models
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(HostnamePattern, HostnamePatternAdmin)
admin.site.register(AssetIdType, AssetIdTypeAdmin)
admin.site.register(Hostname, HostnameAdmin)
