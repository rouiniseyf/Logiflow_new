from rest_framework.response import Response
from rest_framework import viewsets,filters,status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_flex_fields import is_expanded
from app.serializers import *
from bareme.serializers import *
from reference.serializers import *
from billing.serializers import *
from reporting.serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class VisiteGroupageViewSet(viewsets.ModelViewSet):
    queryset = VisiteGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = VisiteGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= VisiteGroupageFilter


    def get_queryset(self):
        queryset = VisiteGroupage.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
        if is_expanded(self.request, 'sous_article'):
            queryset = queryset.prefetch_related('sous_article')
        if is_expanded(self.request, 'transitaire'):
            queryset = queryset.prefetch_related('transitaire')
        return queryset


    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset = self.filter_queryset(self.get_queryset())
            deleted, _ = queryset.filter(pk__in=ids).delete()
            if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
            else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PositionGroupageViewSet(viewsets.ModelViewSet):
    queryset = PositionGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PositionGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PositionGroupageFilter


    def get_queryset(self):
        queryset = PositionGroupage.objects.all()
        if is_expanded(self.request, 'sous_article'):
            queryset = queryset.prefetch_related('sous_article')
        if is_expanded(self.request, 'box'):
            queryset = queryset.prefetch_related('box')
        return queryset


    def list(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the request query parameters
        if request.query_params.get('all', False):
            # If 'all' is present, return all records without pagination
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # If 'all' is not present, proceed with pagination as usual
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not ids:
           return Response({'detail': 'No IDs provided for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset = self.filter_queryset(self.get_queryset())
            deleted, _ = queryset.filter(pk__in=ids).delete()
            if deleted > 0:
               return Response({'detail': f'Successfully deleted objects with ids: {ids} .'}, status=status.HTTP_204_NO_CONTENT)
            else:
               return Response({'detail': 'No objects found for deletion.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
           return Response({'detail': f'Error during deletion: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


