from django.utils import timezone
from rest_framework import serializers
from api.modules.parameter.parameter_model import Parameter


class ParameterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'code', 'description',
                  'is_deleted', 'created_at', 'updated_at', 'deleted_at']


class ParameterSerializer(serializers.ModelSerializer):

    def update(self, parameter, validated_data):
        parameter.code = validated_data.get(
            'code', parameter.code)
        parameter.description = validated_data.get(
            'description', parameter.description)
        parameter.updated_at = timezone.now()
        parameter.is_deleted = validated_data.get(
            'is_deleted', parameter.is_deleted)
        parameter.save()
        return parameter

    class Meta:
        model = Parameter
        depth = 1
        fields = ['id', 'code', 'description',
                  'is_deleted', 'created_at', 'updated_at', 'deleted_at']
