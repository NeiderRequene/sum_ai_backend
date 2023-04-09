from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)

from api.modules.user.models.user_model import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD
