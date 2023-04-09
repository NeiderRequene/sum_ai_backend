
from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'
