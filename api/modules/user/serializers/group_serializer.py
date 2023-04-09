
from django.contrib.auth.models import Group
from rest_framework import serializers

from api.modules.user.serializers.permission_serializer import PermissionSerializer


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
