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

    # ajax views

]
