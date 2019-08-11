from django.contrib import admin

# import models
from hostmgr.models import (Owner,
                            Project,
                            HostnamePattern,
                            AssetIdType,
                            Hostname
                            )


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'is_active', 'name', 'group', 'email']
    search_fields = ['name', 'email']
    list_filter = ['is_active', 'group']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'is_active', 'name', 'owner', 'description']
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'owner']


class HostnamePatternAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'is_active', 'name', 'description', 'project', 'prefix', 'delimiter', 'max_hosts', 'increment', 'start_from']
    search_fields = ['name', 'description', 'prefix', 'delimiter', 'max_hosts', 'increment', 'start_from']
    list_filter = ['is_active', 'project']


class AssetIdTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'is_active', 'name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['is_active']


class HostnameAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'is_active', 'pattern', 'hostname', 'asset_id', 'asset_id_type', 'is_eternal', 'status', 'reservation_expires', 'assignment_expires']
    search_fields = ['hostname', 'asset_id', 'status']
    list_filter = ['is_active', 'pattern', 'asset_id_type', 'is_eternal', 'status']


# register models
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(HostnamePattern, HostnamePatternAdmin)
admin.site.register(AssetIdType, AssetIdTypeAdmin)
admin.site.register(Hostname, HostnameAdmin)
