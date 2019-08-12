from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

# import views
import hostmgr.views.views_gui as gui
import hostmgr.views.views_api as api
import hostmgr.views.views_ajax as ajax

app_name = 'hostmgr'

router = DefaultRouter()

urlpatterns = [
    # list views
    path('list_owners/', gui.ListOwners.as_view(), name='list_owners'),
    path('list_projects/', gui.ListProjects.as_view(), name='list_projects'),
    path('list_patterns/', gui.ListPatterns.as_view(), name='list_patterns'),
    path('list_hostnames/', gui.ListHostnames.as_view(), name='list_hostnames'),

    # detail views
    path('detail_owner/<int:pk>/', gui.DetailOwner.as_view(), name='detail_owner'),
    path('detail_project/<int:pk>/', gui.DetailProject.as_view(), name='detail_project'),
    path('detail_pattern/<int:pk>/', gui.DetailPattern.as_view(), name='detail_pattern'),

    # custom views
    path('show_admin_panel/', gui.ShowAdminPanel.as_view(), name='show_admin_panel'),

    # ajax views
    path('get_owner_details', ajax.get_owner_details, name='get_owner_details'),
    path('get_project_details', ajax.get_project_details, name='get_project_details'),
    path('get_pattern_details', ajax.get_pattern_details, name='get_pattern_details'),
    path('get_hostname_details', ajax.get_hostname_details, name='get_hostname_details'),

]
