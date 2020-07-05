from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

# import views
import hostmgr.views.views_api as api


app_name = 'api'

router = DefaultRouter()

# hostmgr API Endpoints
router.register(r'owner', api.OwnerViewSet, 'owner')
router.register(r'project', api.ProjectViewSet, 'project')
router.register(r'pattern', api.PatternViewSet, 'pattern')
router.register(r'assetidtype', api.AssetIdTypeViewSet, 'assetidtype')
router.register(r'hostname', api.HostnameViewSet, 'hostname')


urlpatterns = [
    # API views
    path('', include(router.urls)),
    path('v1/', include(router.urls)),
]
