from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import CustomTokenObtainPairSerializer

# Create your views here.


class EmailTokenObtainPairView(TokenObtainPairView):
    """Vista para activar el login con email y password

    Args:
        TokenObtainPairView (_type_): Clase para obtener el token de autenticación
    """
    serializer_class = CustomTokenObtainPairSerializer
