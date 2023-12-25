from rest_framework.response import Response
from rest_framework import viewsets,filters,status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_flex_fields import is_expanded
from app.serializers import *
from reference.serializers import *
from billing.serializers import *
from reporting.serializers import *
from groupage.serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BaremeViewSet(viewsets.ModelViewSet):
    queryset = Bareme.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BaremeSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BaremeFilter


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


class RegimeViewSet(viewsets.ModelViewSet):
    queryset = Regime.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = RegimeSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= RegimeFilter


    def get_queryset(self):
        queryset = Regime.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'parc'):
            queryset = queryset.prefetch_related('parc')
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


class RubriqueViewSet(viewsets.ModelViewSet):
    queryset = Rubrique.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = RubriqueSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= RubriqueFilter


    def get_queryset(self):
        queryset = Rubrique.objects.all()
        if is_expanded(self.request, 'direction'):
            queryset = queryset.prefetch_related('direction')
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


class PrestationViewSet(viewsets.ModelViewSet):
    queryset = Prestation.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PrestationSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PrestationFilter


    def get_queryset(self):
        queryset = Prestation.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'rubrique'):
            queryset = queryset.prefetch_related('rubrique')
        if is_expanded(self.request, 'type_tc'):
            queryset = queryset.prefetch_related('type_tc')
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


class PrestationOccasionnelleViewSet(viewsets.ModelViewSet):
    queryset = PrestationOccasionnelle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PrestationOccasionnelleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PrestationOccasionnelleFilter


    def get_queryset(self):
        queryset = PrestationOccasionnelle.objects.all()
        if is_expanded(self.request, 'tc'):
            queryset = queryset.prefetch_related('tc')
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


class PrestationOccasionnelleGroupageViewSet(viewsets.ModelViewSet):
    queryset = PrestationOccasionnelleGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PrestationOccasionnelleGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PrestationOccasionnelleGroupageFilter


    def get_queryset(self):
        queryset = PrestationOccasionnelleGroupage.objects.all()
        if is_expanded(self.request, 'sous_article'):
            queryset = queryset.prefetch_related('sous_article')
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


class PrestationArticleViewSet(viewsets.ModelViewSet):
    queryset = PrestationArticle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PrestationArticleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PrestationArticleFilter


    def get_queryset(self):
        queryset = PrestationArticle.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'rubrique'):
            queryset = queryset.prefetch_related('rubrique')
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


class SejourViewSet(viewsets.ModelViewSet):
    queryset = Sejour.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = SejourSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= SejourFilter


    def get_queryset(self):
        queryset = Sejour.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'type_tc'):
            queryset = queryset.prefetch_related('type_tc')
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


class SejourTcGroupageViewSet(viewsets.ModelViewSet):
    queryset = SejourTcGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = SejourTcGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= SejourTcGroupageFilter


    def get_queryset(self):
        queryset = SejourTcGroupage.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'type_tc'):
            queryset = queryset.prefetch_related('type_tc')
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


class SejourSousArticleGroupageViewSet(viewsets.ModelViewSet):
    queryset = SejourSousArticleGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = SejourSousArticleGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= SejourSousArticleGroupageFilter


    def get_queryset(self):
        queryset = SejourSousArticleGroupage.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
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


class BranchementViewSet(viewsets.ModelViewSet):
    queryset = Branchement.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BranchementSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BranchementFilter


    def get_queryset(self):
        queryset = Branchement.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'type_tc'):
            queryset = queryset.prefetch_related('type_tc')
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


class PrestationGroupageViewSet(viewsets.ModelViewSet):
    queryset = PrestationGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PrestationGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PrestationGroupageFilter


    def get_queryset(self):
        queryset = PrestationGroupage.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'rubrique'):
            queryset = queryset.prefetch_related('rubrique')
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


class PrestationVisiteGroupageViewSet(viewsets.ModelViewSet):
    queryset = PrestationVisiteGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PrestationVisiteGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PrestationVisiteGroupageFilter


    def get_queryset(self):
        queryset = PrestationVisiteGroupage.objects.all()
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
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


