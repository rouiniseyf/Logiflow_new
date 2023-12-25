from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet 
import django_filters
from .models import * 
from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'page'


class LignePrestationFilter(FilterSet): 
    rubrique_object__direction__ids = django_filters.BaseInFilter(
        field_name='rubrique_object__direction__id',
        lookup_expr='in',
        method='filter_rubrique_object__direction__ids')
        
    
    def filter_rubrique_object__direction__ids(self, queryset, name, value):        
        return queryset.filter(rubrique_object__direction__id__in=value)
    
    class Meta: 
        model = LignePrestation 
        fields ={
            'proforma__date_proforma' : ['gte','lte'],
            'proforma__valide' : ['exact'],
            'rubrique_object': ['exact'], 
        }

class LignePrestationGroupageFilter(FilterSet): 
    rubrique_object__direction__ids = django_filters.BaseInFilter(
        field_name='rubrique_object__direction__id',
        lookup_expr='in',
        method='filter_rubrique_object__direction__ids')
        
    
    def filter_rubrique_object__direction__ids(self, queryset, name, value):        
        return queryset.filter(rubrique_object__direction__id__in=value)
    
    class Meta: 
        model = LigneProformaGroupage 
        fields ={
            'proforma__date_proforma' : ['gte','lte'],
            'rubrique_object': ['exact'], 
            'proforma__valide' : ['exact'],
        }


class FactureFilter(FilterSet): 
    class Meta: 
        model = Facture 
        fields ={
            'proforma__date_proforma' : ['gte','lte'],
            'proforma__gros__id' : ['exact'],
            'proforma__article__client__id' : ['exact'],
            'proforma__article__id' : ['exact']
        }

class FactureGroupageFilter(FilterSet): 
    
    class Meta: 
        model = FactureGroupage 
        fields ={
            'proforma__date_proforma' : ['gte','lte'],
            'proforma__gros__id' : ['exact'],
            'proforma__article__id' : ['exact'],
            'proforma__article__client__id' : ['exact'],

        }