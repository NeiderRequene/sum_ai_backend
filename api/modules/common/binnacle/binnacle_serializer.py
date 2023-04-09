from rest_framework import serializers
from api.modules.common.binnacle.binnacle_model import Binnacle


class BinnacleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Binnacle
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at')
