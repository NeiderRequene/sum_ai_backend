from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.filters import APIFilters

from api.modules.user.models.user_model import User

from api.modules.user.serializers.user_serializer import UserCreateSerializer, UserDetailSerializer, UserListSerializer
from api.pagination import PaginationHandlerMixin, StandardResultsSetPagination
from api.permissions import IsAdmin, IsAdminOrUser


class UserListViewSet(APIView, PaginationHandlerMixin):
    """
    Vista para obtener el listado de usuarios.
    """
    http_method_names = ['get']
    pagination_class = StandardResultsSetPagination
    serializer_class = UserListSerializer
    filter_fields = {
        'id': ["in", "exact"],
        'is_active': ['exact'],
        'name': ["icontains"],
        'first_name': ['icontains'],
        'last_name': ['icontains'],
        'email': ["exact"],
        'groups__name': ['exact', 'contains'],
    }
    permission_classes = [
        permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            users = User.objects.all().order_by('-date_joined')
            user_filter = APIFilters()
            filtered_queryset = user_filter.filter_queryset(
                request, users, self)
            if (request.query_params.get('data_all') is not None and request.query_params.get('data_all') == "YES"):
                serializer = self.serializer_class(
                    filtered_queryset, many=True)
                return Response({
                    'count': len(filtered_queryset),
                    'next': None,
                    'previous': None,
                    'results': serializer.data
                }, status=status.HTTP_200_OK)
            page = self.paginate_queryset(filtered_queryset)
            if page is not None:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterViewSet(APIView, PaginationHandlerMixin):
    """
    Vista para registrar un usuario con email y password.
    """
    http_method_names = ['post']
    serializer_class = UserCreateSerializer
    permission_classes = [
        permissions.AllowAny]

    def post(self, request):
        try:
            if ('user_group' in request.data):
                user_group = Group.objects.get(name=request.data['user_group'])
            serializer = UserCreateSerializer(
                data={**request.data, "groups": [user_group.pk]})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailViewSet(APIView):
    """
    Vista para mostrar el detalle de usuario específico.
    Además, permite actualizar los datos de un usuario
    """
    permission_classes = [
        permissions.IsAuthenticated, IsAdminOrUser]
    http_method_names = ['get', 'put']

    def get_object(self, id):
        return User.objects.get(pk=id)

    def get(self, request, id, format=None):
        try:
            user = self.get_object(id)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'No se encontró al usuario.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            user = self.get_object(id)
            serializer = UserDetailSerializer(
                user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'No se encontró al usuario.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as identifier:
            print('identifier', identifier)
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)


class UserAuthViewSet(APIView):
    """
    Vista para ver un usuario, por el token de autenticacion.
    """
    permission_classes = [
        permissions.IsAuthenticated, IsAdminOrUser]
    http_method_names = ['get']

    def get_object(self, id):
        return User.objects.get(pk=id)

    def get(self, request, format=None):
        try:
            user = self.get_object(request.user.id)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as identifier:
            print('identifier 💥', identifier)
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAuthViewSet(APIView):
    """
    Vista para eliminar un usuario, por el token de autenticacion.
    """
    permission_classes = [
        permissions.IsAuthenticated, IsAdminOrUser]
    http_method_names = ['delete']

    def get_object(self, id):
        return User.objects.get(pk=id)

    def delete(self, request):
        try:
            user = self.get_object(request.user.id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'No se encontró el usuario.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)
