from rest_framework import mixins, filters, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import pagination
from ..models import Tc, Gros 
from ..serializers import *
from ..filters import *
from rest_framework import viewsets

class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 10
    page_query_param = 'page'



class TcList(generics.ListAPIView,generics.GenericAPIView): 

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['tc',] 
    filterset_class= TcFilter
    permission_classes = [AllowAny]
    queryset = Tc.objects.all().order_by("-id")  
    serializer_class = TcSerializer 

    # ordering_fields = ['date',  ]

    def get(self, request, *args, **kwargs): 
        return self.list(request, *args, **kwargs)



class GrosList(generics.ListAPIView,generics.GenericAPIView): 

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['designation','id',] 
    permission_classes = [AllowAny]
    queryset = Gros.objects.all().order_by("-id")  
    serializer_class = GrosSerializer 
    filterset_class= GrosFilter


    # ordering_fields = ['date',  ]

    def get(self, request, *args, **kwargs): 
        return self.list(request, *args, **kwargs)


class ArticleList(generics.ListAPIView,generics.GenericAPIView): 

    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    permission_classes = [AllowAny]
    queryset = Article.objects.all().order_by("-id")  
    serializer_class = ArticleSerializer 
    filterset_class= ArticleFilter


    # ordering_fields = ['date',  ]

    def get(self, request, *args, **kwargs): 
        return self.list(request, *args, **kwargs)
