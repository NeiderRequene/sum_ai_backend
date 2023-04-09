from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.filters import APIFilters
from api.modules.parameter.parameter_model import Parameter
from api.modules.parameter.parameter_serializer import ParameterSerializer


from api.pagination import PaginationHandlerMixin, StandardResultsSetPagination
from django.utils import timezone

from api.permissions import IsAdminOrUser


class ParameterViewSet(APIView, PaginationHandlerMixin):
    """
    Vista para manejar los parametros globales.
    """
    permission_classes = [permissions.IsAuthenticated,
                          IsAdminOrUser]
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = StandardResultsSetPagination
    serializer_class = ParameterSerializer
    filter_fields = {
        'id': ["in", "exact"],
        'code': ['exact'],
        'description': ['icontains'],
        'created_at': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }

    def get(self, request):
        try:
            # Retorna un sólo registro por su id
            if (request.query_params.get('id') is not None):
                parameter = self.get_object(
                    request.query_params.get('id'))
                serializer = ParameterSerializer(
                    parameter)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            parameters = Parameter.objects.filter(
                is_deleted=False).all().order_by('-created_at')
            filters = APIFilters()
            filtered_queryset = filters.filter_queryset(
                request, parameters, self)
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
                serializer = self.serializer_class(
                    parameters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = ParameterSerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as identifier:
            print('error 💥', identifier)
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, id):
        return Parameter.objects.get(pk=id)

    def put(self, request):
        try:
            if 'id' not in request.data:
                return Response({'message': 'El id del parameter es requerido.'}, status=status.HTTP_404_NOT_FOUND)
            parameter = self.get_object(request.data['id'])
            serializer = ParameterSerializer(
                parameter, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Parameter.DoesNotExist:
            return Response({'message': 'No se encontró el parameter.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            parameter = self.get_object(id)
            parameter.is_deleted = True
            parameter.updated_at = timezone.now()
            parameter.deleted_at = timezone.now()
            parameter.save()
            serializer = ParameterSerializer(
                parameter)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Parameter.DoesNotExist:
            return Response({'message': 'No se encontró el parameter.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)


class ParameterPublicViewSet(APIView, PaginationHandlerMixin):
    """
    Vista para manejar los parametros globales.
    """
    permission_classes = [permissions.AllowAny, ]
    http_method_names = ['get']
    pagination_class = StandardResultsSetPagination
    serializer_class = ParameterSerializer
    filter_fields = {
        'id': ["in", "exact"],
        'code': ['exact'],
        'description': ['icontains'],
        'created_at': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }

    def get(self, request):
        try:
            # Retorna un sólo registro por su id
            if (request.query_params.get('id') is not None):
                parameter = self.get_object(
                    request.query_params.get('id'))
                serializer = ParameterSerializer(
                    parameter)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            parameters = Parameter.objects.filter(
                is_deleted=False).all().order_by('-created_at')
            filters = APIFilters()
            filtered_queryset = filters.filter_queryset(
                request, parameters, self)
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
                serializer = self.serializer_class(
                    parameters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as identifier:
            return Response({'message': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)
