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
from reporting.serializers import *
from groupage.serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ProformaViewSet(viewsets.ModelViewSet):
    queryset = Proforma.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = ProformaSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= ProformaFilter


    def get_queryset(self):
        queryset = Proforma.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
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


class GroupeViewSet(viewsets.ModelViewSet):
    queryset = Groupe.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = GroupeSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= GroupeFilter


    def get_queryset(self):
        queryset = Groupe.objects.all()
        if is_expanded(self.request, 'proforma'):
            queryset = queryset.prefetch_related('proforma')
        if is_expanded(self.request, 'type'):
            queryset = queryset.prefetch_related('type')
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


class GroupeLigneViewSet(viewsets.ModelViewSet):
    queryset = GroupeLigne.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = GroupeLigneSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= GroupeLigneFilter


    def get_queryset(self):
        queryset = GroupeLigne.objects.all()
        if is_expanded(self.request, 'groupe'):
            queryset = queryset.prefetch_related('groupe')
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


class LignePrestationViewSet(viewsets.ModelViewSet):
    queryset = LignePrestation.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = LignePrestationSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= LignePrestationFilter


    def get_queryset(self):
        queryset = LignePrestation.objects.all()
        if is_expanded(self.request, 'proforma'):
            queryset = queryset.prefetch_related('proforma')
        if is_expanded(self.request, 'groupe'):
            queryset = queryset.prefetch_related('groupe')
        if is_expanded(self.request, 'rubrique_object'):
            queryset = queryset.prefetch_related('rubrique_object')
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


class LignePrestationArticleViewSet(viewsets.ModelViewSet):
    queryset = LignePrestationArticle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = LignePrestationArticleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= LignePrestationArticleFilter


    def get_queryset(self):
        queryset = LignePrestationArticle.objects.all()
        if is_expanded(self.request, 'proforma'):
            queryset = queryset.prefetch_related('proforma')
        if is_expanded(self.request, 'rubrique_object'):
            queryset = queryset.prefetch_related('rubrique_object')
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


class BonCommandeViewSet(viewsets.ModelViewSet):
    queryset = BonCommande.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BonCommandeSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BonCommandeFilter


    def get_queryset(self):
        queryset = BonCommande.objects.all()
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
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


class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = CommandeSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= CommandeFilter


    def get_queryset(self):
        queryset = Commande.objects.all()
        if is_expanded(self.request, 'bon_commande'):
            queryset = queryset.prefetch_related('bon_commande')
        if is_expanded(self.request, 'tc'):
            queryset = queryset.prefetch_related('tc')
        if is_expanded(self.request, 'rubrique_object'):
            queryset = queryset.prefetch_related('rubrique_object')
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


class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = FactureSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= FactureFilter


    def get_queryset(self):
        queryset = Facture.objects.all()
        if is_expanded(self.request, 'proforma'):
            queryset = queryset.prefetch_related('proforma')
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


class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PaiementSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PaiementFilter


    def get_queryset(self):
        queryset = Paiement.objects.all()
        if is_expanded(self.request, 'facture'):
            queryset = queryset.prefetch_related('facture')
        if is_expanded(self.request, 'banque'):
            queryset = queryset.prefetch_related('banque')
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


class FactureComplementaireViewSet(viewsets.ModelViewSet):
    queryset = FactureComplementaire.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = FactureComplementaireSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= FactureComplementaireFilter


    def get_queryset(self):
        queryset = FactureComplementaire.objects.all()
        if is_expanded(self.request, 'facture'):
            queryset = queryset.prefetch_related('facture')
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


class LigneFactureComplementaireViewSet(viewsets.ModelViewSet):
    queryset = LigneFactureComplementaire.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = LigneFactureComplementaireSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= LigneFactureComplementaireFilter


    def get_queryset(self):
        queryset = LigneFactureComplementaire.objects.all()
        if is_expanded(self.request, 'facture_complementaire'):
            queryset = queryset.prefetch_related('facture_complementaire')
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


class PaiementFactureComplementaireViewSet(viewsets.ModelViewSet):
    queryset = PaiementFactureComplementaire.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PaiementFactureComplementaireSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PaiementFactureComplementaireFilter


    def get_queryset(self):
        queryset = PaiementFactureComplementaire.objects.all()
        if is_expanded(self.request, 'facture_complementaire'):
            queryset = queryset.prefetch_related('facture_complementaire')
        if is_expanded(self.request, 'banque'):
            queryset = queryset.prefetch_related('banque')
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


class FactureAvoireViewSet(viewsets.ModelViewSet):
    queryset = FactureAvoire.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = FactureAvoireSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= FactureAvoireFilter


    def get_queryset(self):
        queryset = FactureAvoire.objects.all()
        if is_expanded(self.request, 'facture'):
            queryset = queryset.prefetch_related('facture')
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


class LigneFactureAvoireViewSet(viewsets.ModelViewSet):
    queryset = LigneFactureAvoire.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = LigneFactureAvoireSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= LigneFactureAvoireFilter


    def get_queryset(self):
        queryset = LigneFactureAvoire.objects.all()
        if is_expanded(self.request, 'facture_avoire'):
            queryset = queryset.prefetch_related('facture_avoire')
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


class BonSortieViewSet(viewsets.ModelViewSet):
    queryset = BonSortie.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BonSortieSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BonSortieFilter


    def get_queryset(self):
        queryset = BonSortie.objects.all()
        if is_expanded(self.request, 'facture'):
            queryset = queryset.prefetch_related('facture')
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


class BonSortieItemViewSet(viewsets.ModelViewSet):
    queryset = BonSortieItem.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BonSortieItemSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BonSortieItemFilter


    def get_queryset(self):
        queryset = BonSortieItem.objects.all()
        if is_expanded(self.request, 'bon_sortie'):
            queryset = queryset.prefetch_related('bon_sortie')
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


class FactureLibreViewSet(viewsets.ModelViewSet):
    queryset = FactureLibre.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = FactureLibreSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= FactureLibreFilter


    def get_queryset(self):
        queryset = FactureLibre.objects.all()
        if is_expanded(self.request, 'client'):
            queryset = queryset.prefetch_related('client')
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


class LigneFactureLibreViewSet(viewsets.ModelViewSet):
    queryset = LigneFactureLibre.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = LigneFactureLibreSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= LigneFactureLibreFilter


    def get_queryset(self):
        queryset = LigneFactureLibre.objects.all()
        if is_expanded(self.request, 'facture_libre'):
            queryset = queryset.prefetch_related('facture_libre')
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


class PaiementFactureLibreViewSet(viewsets.ModelViewSet):
    queryset = PaiementFactureLibre.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PaiementFactureLibreSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PaiementFactureLibreFilter


    def get_queryset(self):
        queryset = PaiementFactureLibre.objects.all()
        if is_expanded(self.request, 'facture_libre'):
            queryset = queryset.prefetch_related('facture_libre')
        if is_expanded(self.request, 'banque'):
            queryset = queryset.prefetch_related('banque')
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


class ProformaGroupageViewSet(viewsets.ModelViewSet):
    queryset = ProformaGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = ProformaGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= ProformaGroupageFilter


    def get_queryset(self):
        queryset = ProformaGroupage.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
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


class LigneProformaGroupageViewSet(viewsets.ModelViewSet):
    queryset = LigneProformaGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = LigneProformaGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= LigneProformaGroupageFilter


    def get_queryset(self):
        queryset = LigneProformaGroupage.objects.all()
        if is_expanded(self.request, 'proforma'):
            queryset = queryset.prefetch_related('proforma')
        if is_expanded(self.request, 'rubrique_object'):
            queryset = queryset.prefetch_related('rubrique_object')
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


class FactureGroupageViewSet(viewsets.ModelViewSet):
    queryset = FactureGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = FactureGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= FactureGroupageFilter


    def get_queryset(self):
        queryset = FactureGroupage.objects.all()
        if is_expanded(self.request, 'proforma'):
            queryset = queryset.prefetch_related('proforma')
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


class PaiementGroupageViewSet(viewsets.ModelViewSet):
    queryset = PaiementGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PaiementGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PaiementGroupageFilter


    def get_queryset(self):
        queryset = PaiementGroupage.objects.all()
        if is_expanded(self.request, 'facture'):
            queryset = queryset.prefetch_related('facture')
        if is_expanded(self.request, 'banque'):
            queryset = queryset.prefetch_related('banque')
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


class BonSortieGroupageViewSet(viewsets.ModelViewSet):
    queryset = BonSortieGroupage.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BonSortieGroupageSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BonSortieGroupageFilter


    def get_queryset(self):
        queryset = BonSortieGroupage.objects.all()
        if is_expanded(self.request, 'sous_article'):
            queryset = queryset.prefetch_related('sous_article')
        if is_expanded(self.request, 'facture'):
            queryset = queryset.prefetch_related('facture')
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


