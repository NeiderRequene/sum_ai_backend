from rest_framework import viewsets
from rest_framework import permissions
from api.modules.common.binnacle.binnacle_model import Binnacle
from api.modules.common.binnacle.binnacle_serializer import BinnacleSerializer

from api.permissions import IsAdmin


class BinnacleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          IsAdmin]
    queryset = Binnacle.objects.all()
    serializer_class = BinnacleSerializer
