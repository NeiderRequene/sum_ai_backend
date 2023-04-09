from django.contrib.auth.models import Permission
from rest_framework import permissions, viewsets

from api.modules.user.serializers.permission_serializer import PermissionSerializer
from api.permissions import IsAdmin


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    http_method_names = ['get']
