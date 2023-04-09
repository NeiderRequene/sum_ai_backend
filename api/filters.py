from django_filters import rest_framework as filters
from rest_framework import serializers


class APIFilters(filters.DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)

        if filter_class:
            return filter_class(request.query_params, queryset=queryset, request=request).qs
        return queryset


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(is_deleted=False)
        return super(FilteredListSerializer, self).to_representation(data)


class FilteredNestedStuctureSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        if (type(data) is not list):
            data = data.filter(is_deleted=False)
        return super(FilteredNestedStuctureSerializer, self).to_representation(data)
