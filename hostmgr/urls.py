from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

# import views
import hostmgr.views.views_gui as gui
import hostmgr.views.views_api as apis
import hostmgr.views.views_ajax as ajax

app_name = 'hostmgr'

router = DefaultRouter()

# hostmgr API Endpoints
router.register(r'owner', apis.OwnerViewSet, "owner")
router.register(r'project', apis.ProjectViewSet, "project")
router.register(r'pattern', apis.PatternViewSet, "pattern")
router.register(r'assetidtype', apis.AssetIdTypeViewSet, "assetidtype")
router.register(r'hostname', apis.HostnameViewSet, "hostname")

urlpatterns = [
    # list views
    path('list_owners/', gui.ListOwners.as_view(), name='list_owners'),
    path('list_projects/', gui.ListProjects.as_view(), name='list_projects'),
    path('list_patterns/', gui.ListPatterns.as_view(), name='list_patterns'),
    path('list_hostnames/', gui.ListHostnames.as_view(), name='list_hostnames'),

    # action views
    path('reserve_hostname/', gui.ReserveHostname.as_view(), name='reserve_hostname'),
    path('assign_hostname/', gui.AssignHostname.as_view(), name='assign_hostname'),
    path('release_hostname/', gui.ReleaseHostname.as_view(), name='release_hostname'),

    # detail views
    path('detail_owner/<int:pk>/', gui.DetailOwner.as_view(), name='detail_owner'),
    path('detail_project/<int:pk>/', gui.DetailProject.as_view(), name='detail_project'),
    path('detail_pattern/<int:pk>/', gui.DetailPattern.as_view(), name='detail_pattern'),

    # custom views
    path('show_admin_panel/', gui.ShowAdminPanel.as_view(), name='show_admin_panel'),
    path('show_api_guide/', gui.ShowApiGuideIndex.as_view(), name='show_api_guide'),
    path('show_api_guide_v1_owner/', gui.ShowApiGuideV1Owner.as_view(), name='show_api_guide_v1_owner'),
    path('show_api_guide_v1_project/', gui.ShowApiGuideV1Project.as_view(), name='show_api_guide_v1_project'),
    path('show_api_guide_v1_pattern/', gui.ShowApiGuideV1Pattern.as_view(), name='show_api_guide_v1_pattern'),
    path('show_api_guide_v1_hostname/', gui.ShowApiGuideV1Hostname.as_view(), name='show_api_guide_v1_hostname'),

    # ajax views
    path('get_owner_details', ajax.get_owner_details, name='get_owner_details'),
    path('get_project_details', ajax.get_project_details, name='get_project_details'),
    path('get_pattern_details', ajax.get_pattern_details, name='get_pattern_details'),
    path('get_hostname_details', ajax.get_hostname_details, name='get_hostname_details'),

    path('get_users_per_owner', ajax.get_users_per_owner, name='get_users_per_owner'),
    path('get_projects_per_owner', ajax.get_projects_per_owner, name='get_projects_per_owner'),
    path('get_patterns_per_owner', ajax.get_patterns_per_owner, name='get_patterns_per_owner'),
    path('get_hostnames_per_owner', ajax.get_hostnames_per_owner, name='get_hostnames_per_owner'),

    path('get_patterns_per_project', ajax.get_patterns_per_project, name='get_patterns_per_project'),
    path('get_hostnames_per_project', ajax.get_hostnames_per_project, name='get_hostnames_per_project'),
    path('get_assigned_hostnames_per_project', ajax.get_assigned_hostnames_per_project, name='get_assigned_hostnames_per_project'),
    path('get_availble_hostnames_per_project', ajax.get_available_hostnames_per_project, name='get_available_hostnames_per_project'),
    path('get_expired_hostnames_per_project', ajax.get_expired_hostnames_per_project, name='get_expired_hostnames_per_project'),
    path('get_reserved_hostnames_per_project', ajax.get_reserved_hostnames_per_project, name='get_reserved_hostnames_per_project'),

    path('get_hostnames_per_pattern', ajax.get_hostnames_per_pattern, name='get_hostnames_per_pattern'),
    path('get_assigned_hostnames_per_pattern', ajax.get_assigned_hostnames_per_pattern, name='get_assigned_hostnames_per_pattern'),
    path('get_available_hostnames_per_pattern', ajax.get_available_hostnames_per_pattern, name='get_available_hostnames_per_pattern'),
    path('get_expired_hostnames_per_pattern', ajax.get_expired_hostnames_per_pattern, name='get_expired_hostnames_per_pattern'),
    path('get_reserved_hostnames_per_pattern', ajax.get_reserved_hostnames_per_pattern, name='get_reserved_hostnames_per_pattern'),

    path('get_owner_auditlog', ajax.get_owner_auditlog, name='get_owner_auditlog'),
    path('get_project_auditlog', ajax.get_project_auditlog, name='get_project_auditlog'),
    path('get_pattern_auditlog', ajax.get_pattern_auditlog, name='get_pattern_auditlog'),
    path('get_hostname_auditlog', ajax.get_hostname_auditlog, name='get_hostname_auditlog'),

    # API views
    path('api/', include(router.urls)),
    path('api/v1/', include(router.urls)),

]
