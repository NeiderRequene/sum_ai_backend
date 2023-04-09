from rest_framework import routers
from api.modules.common.binnacle.binnacle_view import BinnacleViewSet

# Importamos las vistas de la app
from api.modules.user.views.group_view import GroupViewSet
from api.modules.user.views.permission_view import PermissionViewSet

router = routers.DefaultRouter()

router.register(r'api/binnacles', BinnacleViewSet)
router.register(r'api/groups', GroupViewSet)
router.register(r'api/permissions', PermissionViewSet)
