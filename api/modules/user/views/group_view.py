from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets

from api.modules.user.serializers.group_serializer import GroupSerializer
from api.permissions import IsAdmin


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
