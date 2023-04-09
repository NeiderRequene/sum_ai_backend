"""
URL configuration for sum_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .router import router

from api.views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from api.modules.user.views.user_view import (
    DeleteUserAuthViewSet,
    UserAuthViewSet,
    UserDetailViewSet,
    UserListViewSet,
    UserRegisterViewSet
)
from api.modules.parameter.parameter_view import (
    ParameterPublicViewSet,
    ParameterViewSet
)

urlpatterns = [
    # 📈 Incluye las rutas definidas en el router.py
    path('', include(router.urls)),

    # 👨‍💻 Routes available to the administrator
    path('admin/', admin.site.urls),

    # 🚀 Rutas para autenticacion
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', EmailTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(r'api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

    # 🙎‍♂️ Rutas del módulo de usuarios
    path('api/users/', UserListViewSet.as_view()),
    path('api/users/register', UserRegisterViewSet.as_view()),
    path('api/users/token', UserAuthViewSet.as_view()),
    path('api/users/delete/', DeleteUserAuthViewSet.as_view()),
    path('api/users/<int:id>/', UserDetailViewSet.as_view()),

    # 🌍 Rutas del módulo de parametros
    path('api/parameters/',
         ParameterViewSet.as_view()),
    path('api/parameters/<int:id>/',
         ParameterViewSet.as_view()),
    path('api/parameters-public/',
         ParameterPublicViewSet.as_view()),
]
