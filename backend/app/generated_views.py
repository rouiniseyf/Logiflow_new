from rest_framework.response import Response
from rest_framework import viewsets,filters,status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_flex_fields import is_expanded


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class GrosViewSet(viewsets.ModelViewSet):
    queryset = Gros.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = GrosSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= GrosFilter


    def create(self, request, *args, **kwargs):
        articles_data = request.data.pop('articles',[])
        # Create nested port_emission 
        port_emission_data = request.data.get('port_emission')
        if isinstance(port_emission_data, int):
            request.data['port_emission'] = port_emission_data
        elif port_emission_data:
            port_emission_serializer = PortSerializer(data=port_emission_data)
            if port_emission_serializer.is_valid():
                port_emission = port_emission_serializer.save()
                request.data['port_emission'] = port_emission.id
            else:
                return Response(port_emission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested port_reception 
        port_reception_data = request.data.get('port_reception')
        if isinstance(port_reception_data, int):
            request.data['port_reception'] = port_reception_data
        elif port_reception_data:
            port_reception_serializer = PortSerializer(data=port_reception_data)
            if port_reception_serializer.is_valid():
                port_reception = port_reception_serializer.save()
                request.data['port_reception'] = port_reception.id
            else:
                return Response(port_reception_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested navire 
        navire_data = request.data.get('navire')
        if isinstance(navire_data, int):
            request.data['navire'] = navire_data
        elif navire_data:
            navire_serializer = NavireSerializer(data=navire_data)
            if navire_serializer.is_valid():
                navire = navire_serializer.save()
                request.data['navire'] = navire.id
            else:
                return Response(navire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested armateur 
        armateur_data = request.data.get('armateur')
        if isinstance(armateur_data, int):
            request.data['armateur'] = armateur_data
        elif armateur_data:
            armateur_serializer = ArmateurSerializer(data=armateur_data)
            if armateur_serializer.is_valid():
                armateur = armateur_serializer.save()
                request.data['armateur'] = armateur.id
            else:
                return Response(armateur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested consignataire 
        consignataire_data = request.data.get('consignataire')
        if isinstance(consignataire_data, int):
            request.data['consignataire'] = consignataire_data
        elif consignataire_data:
            consignataire_serializer = ConsignataireSerializer(data=consignataire_data)
            if consignataire_serializer.is_valid():
                consignataire = consignataire_serializer.save()
                request.data['consignataire'] = consignataire.id
            else:
                return Response(consignataire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested bareme 
        bareme_data = request.data.get('bareme')
        if isinstance(bareme_data, int):
            request.data['bareme'] = bareme_data
        elif bareme_data:
            bareme_serializer = BaremeSerializer(data=bareme_data)
            if bareme_serializer.is_valid():
                bareme = bareme_serializer.save()
                request.data['bareme'] = bareme.id
            else:
                return Response(bareme_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested regime 
        regime_data = request.data.get('regime')
        if isinstance(regime_data, int):
            request.data['regime'] = regime_data
        elif regime_data:
            regime_serializer = RegimeSerializer(data=regime_data)
            if regime_serializer.is_valid():
                regime = regime_serializer.save()
                request.data['regime'] = regime.id
            else:
                return Response(regime_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        gros_serializer = self.get_serializer(data=request.data)
        gros_serializer.is_valid(raise_exception=True)
        gros_instance = gros_serializer.save()


        # Create nested articles


        for article_data in articles_data:
            article_data['gros'] = gros_instance.id
            article_serializer = ArticleSerializer(data=article_data)
            article_serializer.is_valid(raise_exception=True)
            article_serializer.save()


        headers = self.get_success_headers(gros_serializer.data)
        return Response(gros_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested port_emission
        port_emission_data = request.data.pop('port_emission', None)
        if isinstance(port_emission_data, int):
            request.data['port_emission'] = port_emission_data
        elif port_emission_data:
            port_emission_id = port_emission_data.get('id')
            if port_emission_id:
                # If 'id' is present, it's an update
                port_emission_instance = Port.objects.get(id=port_emission_id)
                port_emission_serializer = PortSerializer(port_emission_instance,data=port_emission_data, partial=partial)
                port_emission_serializer.is_valid(raise_exception=True)
                port_emission_serializer.save()
            else:
                # If 'id' is not present, it's a create
                port_emission_serializer = PortSerializer(data=port_emission_data)
                port_emission_serializer.is_valid(raise_exception=True)
                port_emission = port_emission_serializer.save()
                request.data['port_emission'] = port_emission.id


        # Update nested port_reception
        port_reception_data = request.data.pop('port_reception', None)
        if isinstance(port_reception_data, int):
            request.data['port_reception'] = port_reception_data
        elif port_reception_data:
            port_reception_id = port_reception_data.get('id')
            if port_reception_id:
                # If 'id' is present, it's an update
                port_reception_instance = Port.objects.get(id=port_reception_id)
                port_reception_serializer = PortSerializer(port_reception_instance,data=port_reception_data, partial=partial)
                port_reception_serializer.is_valid(raise_exception=True)
                port_reception_serializer.save()
            else:
                # If 'id' is not present, it's a create
                port_reception_serializer = PortSerializer(data=port_reception_data)
                port_reception_serializer.is_valid(raise_exception=True)
                port_reception = port_reception_serializer.save()
                request.data['port_reception'] = port_reception.id


        # Update nested navire
        navire_data = request.data.pop('navire', None)
        if isinstance(navire_data, int):
            request.data['navire'] = navire_data
        elif navire_data:
            navire_id = navire_data.get('id')
            if navire_id:
                # If 'id' is present, it's an update
                navire_instance = Navire.objects.get(id=navire_id)
                navire_serializer = NavireSerializer(navire_instance,data=navire_data, partial=partial)
                navire_serializer.is_valid(raise_exception=True)
                navire_serializer.save()
            else:
                # If 'id' is not present, it's a create
                navire_serializer = NavireSerializer(data=navire_data)
                navire_serializer.is_valid(raise_exception=True)
                navire = navire_serializer.save()
                request.data['navire'] = navire.id


        # Update nested armateur
        armateur_data = request.data.pop('armateur', None)
        if isinstance(armateur_data, int):
            request.data['armateur'] = armateur_data
        elif armateur_data:
            armateur_id = armateur_data.get('id')
            if armateur_id:
                # If 'id' is present, it's an update
                armateur_instance = Armateur.objects.get(id=armateur_id)
                armateur_serializer = ArmateurSerializer(armateur_instance,data=armateur_data, partial=partial)
                armateur_serializer.is_valid(raise_exception=True)
                armateur_serializer.save()
            else:
                # If 'id' is not present, it's a create
                armateur_serializer = ArmateurSerializer(data=armateur_data)
                armateur_serializer.is_valid(raise_exception=True)
                armateur = armateur_serializer.save()
                request.data['armateur'] = armateur.id


        # Update nested consignataire
        consignataire_data = request.data.pop('consignataire', None)
        if isinstance(consignataire_data, int):
            request.data['consignataire'] = consignataire_data
        elif consignataire_data:
            consignataire_id = consignataire_data.get('id')
            if consignataire_id:
                # If 'id' is present, it's an update
                consignataire_instance = Consignataire.objects.get(id=consignataire_id)
                consignataire_serializer = ConsignataireSerializer(consignataire_instance,data=consignataire_data, partial=partial)
                consignataire_serializer.is_valid(raise_exception=True)
                consignataire_serializer.save()
            else:
                # If 'id' is not present, it's a create
                consignataire_serializer = ConsignataireSerializer(data=consignataire_data)
                consignataire_serializer.is_valid(raise_exception=True)
                consignataire = consignataire_serializer.save()
                request.data['consignataire'] = consignataire.id


        # Update nested bareme
        bareme_data = request.data.pop('bareme', None)
        if isinstance(bareme_data, int):
            request.data['bareme'] = bareme_data
        elif bareme_data:
            bareme_id = bareme_data.get('id')
            if bareme_id:
                # If 'id' is present, it's an update
                bareme_instance = Bareme.objects.get(id=bareme_id)
                bareme_serializer = BaremeSerializer(bareme_instance,data=bareme_data, partial=partial)
                bareme_serializer.is_valid(raise_exception=True)
                bareme_serializer.save()
            else:
                # If 'id' is not present, it's a create
                bareme_serializer = BaremeSerializer(data=bareme_data)
                bareme_serializer.is_valid(raise_exception=True)
                bareme = bareme_serializer.save()
                request.data['bareme'] = bareme.id


        # Update nested regime
        regime_data = request.data.pop('regime', None)
        if isinstance(regime_data, int):
            request.data['regime'] = regime_data
        elif regime_data:
            regime_id = regime_data.get('id')
            if regime_id:
                # If 'id' is present, it's an update
                regime_instance = Regime.objects.get(id=regime_id)
                regime_serializer = RegimeSerializer(regime_instance,data=regime_data, partial=partial)
                regime_serializer.is_valid(raise_exception=True)
                regime_serializer.save()
            else:
                # If 'id' is not present, it's a create
                regime_serializer = RegimeSerializer(data=regime_data)
                regime_serializer.is_valid(raise_exception=True)
                regime = regime_serializer.save()
                request.data['regime'] = regime.id


        gros_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        gros_serializer.is_valid(raise_exception=True)
        gros_instance = gros_serializer.save()


        # Update nested articles 
        articles_data = request.data.pop('articles', [])
        if articles_data:
            for article_data in articles_data:
                if isinstance(article_data, int):
                    pass
                else: 
                    article_id = articles_data.get('id')
                    if article_id:
                        # If 'id' is present, it's an update
                        articles_instance = Article.objects.get(id=article_id)
                        articles_serializer = ArticleSerializer(articles_instance, data=articles_data, partial=partial)
                    else:
                        # If 'id' is not present, it's a create
                        articles_data['gros'] = gros_instance.id
                        articles_serializer = ArticleSerializer(data=articles_data)
                    articles_serializer.is_valid(raise_exception=True)
                    articles_serializer.save()
        return Response(gros_serializer.data)


    def get_queryset(self):
        queryset = Gros.objects.all()
        if is_expanded(self.request, 'port_emission'):
            queryset = queryset.prefetch_related('port_emission')
        if is_expanded(self.request, 'port_reception'):
            queryset = queryset.prefetch_related('port_reception')
        if is_expanded(self.request, 'navire'):
            queryset = queryset.prefetch_related('navire')
        if is_expanded(self.request, 'armateur'):
            queryset = queryset.prefetch_related('armateur')
        if is_expanded(self.request, 'consignataire'):
            queryset = queryset.prefetch_related('consignataire')
        if is_expanded(self.request, 'bareme'):
            queryset = queryset.prefetch_related('bareme')
        if is_expanded(self.request, 'regime'):
            queryset = queryset.prefetch_related('regime')
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


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= ArticleFilter


    def create(self, request, *args, **kwargs):
        # Create nested gros 
        gros_data = request.data.get('gros')
        if isinstance(gros_data, int):
            request.data['gros'] = gros_data
        elif gros_data:
            gros_serializer = GrosSerializer(data=gros_data)
            if gros_serializer.is_valid():
                gros = gros_serializer.save()
                request.data['gros'] = gros.id
            else:
                return Response(gros_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested client 
        client_data = request.data.get('client')
        if isinstance(client_data, int):
            request.data['client'] = client_data
        elif client_data:
            client_serializer = ClientSerializer(data=client_data)
            if client_serializer.is_valid():
                client = client_serializer.save()
                request.data['client'] = client.id
            else:
                return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested transitaire 
        transitaire_data = request.data.get('transitaire')
        if isinstance(transitaire_data, int):
            request.data['transitaire'] = transitaire_data
        elif transitaire_data:
            transitaire_serializer = TransitaireSerializer(data=transitaire_data)
            if transitaire_serializer.is_valid():
                transitaire = transitaire_serializer.save()
                request.data['transitaire'] = transitaire.id
            else:
                return Response(transitaire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        article_serializer = self.get_serializer(data=request.data)
        article_serializer.is_valid(raise_exception=True)
        article_instance = article_serializer.save()


        headers = self.get_success_headers(article_serializer.data)
        return Response(article_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested gros
        gros_data = request.data.pop('gros', None)
        if isinstance(gros_data, int):
            request.data['gros'] = gros_data
        elif gros_data:
            gros_id = gros_data.get('id')
            if gros_id:
                # If 'id' is present, it's an update
                gros_instance = Gros.objects.get(id=gros_id)
                gros_serializer = GrosSerializer(gros_instance,data=gros_data, partial=partial)
                gros_serializer.is_valid(raise_exception=True)
                gros_serializer.save()
            else:
                # If 'id' is not present, it's a create
                gros_serializer = GrosSerializer(data=gros_data)
                gros_serializer.is_valid(raise_exception=True)
                gros = gros_serializer.save()
                request.data['gros'] = gros.id


        # Update nested client
        client_data = request.data.pop('client', None)
        if isinstance(client_data, int):
            request.data['client'] = client_data
        elif client_data:
            client_id = client_data.get('id')
            if client_id:
                # If 'id' is present, it's an update
                client_instance = Client.objects.get(id=client_id)
                client_serializer = ClientSerializer(client_instance,data=client_data, partial=partial)
                client_serializer.is_valid(raise_exception=True)
                client_serializer.save()
            else:
                # If 'id' is not present, it's a create
                client_serializer = ClientSerializer(data=client_data)
                client_serializer.is_valid(raise_exception=True)
                client = client_serializer.save()
                request.data['client'] = client.id


        # Update nested transitaire
        transitaire_data = request.data.pop('transitaire', None)
        if isinstance(transitaire_data, int):
            request.data['transitaire'] = transitaire_data
        elif transitaire_data:
            transitaire_id = transitaire_data.get('id')
            if transitaire_id:
                # If 'id' is present, it's an update
                transitaire_instance = Transitaire.objects.get(id=transitaire_id)
                transitaire_serializer = TransitaireSerializer(transitaire_instance,data=transitaire_data, partial=partial)
                transitaire_serializer.is_valid(raise_exception=True)
                transitaire_serializer.save()
            else:
                # If 'id' is not present, it's a create
                transitaire_serializer = TransitaireSerializer(data=transitaire_data)
                transitaire_serializer.is_valid(raise_exception=True)
                transitaire = transitaire_serializer.save()
                request.data['transitaire'] = transitaire.id


        article_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        article_serializer.is_valid(raise_exception=True)
        article_instance = article_serializer.save()


        return Response(article_serializer.data)


    def get_queryset(self):
        queryset = Article.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'client'):
            queryset = queryset.prefetch_related('client')
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


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = PositionSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= PositionFilter


    def create(self, request, *args, **kwargs):
        # Create nested parc 
        parc_data = request.data.get('parc')
        if isinstance(parc_data, int):
            request.data['parc'] = parc_data
        elif parc_data:
            parc_serializer = ParcSerializer(data=parc_data)
            if parc_serializer.is_valid():
                parc = parc_serializer.save()
                request.data['parc'] = parc.id
            else:
                return Response(parc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested zone 
        zone_data = request.data.get('zone')
        if isinstance(zone_data, int):
            request.data['zone'] = zone_data
        elif zone_data:
            zone_serializer = ZoneSerializer(data=zone_data)
            if zone_serializer.is_valid():
                zone = zone_serializer.save()
                request.data['zone'] = zone.id
            else:
                return Response(zone_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested tc 
        tc_data = request.data.get('tc')
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_serializer = TcSerializer(data=tc_data)
            if tc_serializer.is_valid():
                tc = tc_serializer.save()
                request.data['tc'] = tc.id
            else:
                return Response(tc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        position_serializer = self.get_serializer(data=request.data)
        position_serializer.is_valid(raise_exception=True)
        position_instance = position_serializer.save()


        headers = self.get_success_headers(position_serializer.data)
        return Response(position_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested parc
        parc_data = request.data.pop('parc', None)
        if isinstance(parc_data, int):
            request.data['parc'] = parc_data
        elif parc_data:
            parc_id = parc_data.get('id')
            if parc_id:
                # If 'id' is present, it's an update
                parc_instance = Parc.objects.get(id=parc_id)
                parc_serializer = ParcSerializer(parc_instance,data=parc_data, partial=partial)
                parc_serializer.is_valid(raise_exception=True)
                parc_serializer.save()
            else:
                # If 'id' is not present, it's a create
                parc_serializer = ParcSerializer(data=parc_data)
                parc_serializer.is_valid(raise_exception=True)
                parc = parc_serializer.save()
                request.data['parc'] = parc.id


        # Update nested zone
        zone_data = request.data.pop('zone', None)
        if isinstance(zone_data, int):
            request.data['zone'] = zone_data
        elif zone_data:
            zone_id = zone_data.get('id')
            if zone_id:
                # If 'id' is present, it's an update
                zone_instance = Zone.objects.get(id=zone_id)
                zone_serializer = ZoneSerializer(zone_instance,data=zone_data, partial=partial)
                zone_serializer.is_valid(raise_exception=True)
                zone_serializer.save()
            else:
                # If 'id' is not present, it's a create
                zone_serializer = ZoneSerializer(data=zone_data)
                zone_serializer.is_valid(raise_exception=True)
                zone = zone_serializer.save()
                request.data['zone'] = zone.id


        # Update nested tc
        tc_data = request.data.pop('tc', None)
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_id = tc_data.get('id')
            if tc_id:
                # If 'id' is present, it's an update
                tc_instance = Tc.objects.get(id=tc_id)
                tc_serializer = TcSerializer(tc_instance,data=tc_data, partial=partial)
                tc_serializer.is_valid(raise_exception=True)
                tc_serializer.save()
            else:
                # If 'id' is not present, it's a create
                tc_serializer = TcSerializer(data=tc_data)
                tc_serializer.is_valid(raise_exception=True)
                tc = tc_serializer.save()
                request.data['tc'] = tc.id


        position_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        position_serializer.is_valid(raise_exception=True)
        position_instance = position_serializer.save()


        return Response(position_serializer.data)


    def get_queryset(self):
        queryset = Position.objects.all()
        if is_expanded(self.request, 'parc'):
            queryset = queryset.prefetch_related('parc')
        if is_expanded(self.request, 'zone'):
            queryset = queryset.prefetch_related('zone')
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


class BulletinsEscortViewSet(viewsets.ModelViewSet):
    queryset = BulletinsEscort.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = BulletinsEscortSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= BulletinsEscortFilter


    def create(self, request, *args, **kwargs):
        # Create nested gros 
        gros_data = request.data.get('gros')
        if isinstance(gros_data, int):
            request.data['gros'] = gros_data
        elif gros_data:
            gros_serializer = GrosSerializer(data=gros_data)
            if gros_serializer.is_valid():
                gros = gros_serializer.save()
                request.data['gros'] = gros.id
            else:
                return Response(gros_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested charge_chargement 
        charge_chargement_data = request.data.get('charge_chargement')
        if isinstance(charge_chargement_data, int):
            request.data['charge_chargement'] = charge_chargement_data
        elif charge_chargement_data:
            charge_chargement_serializer = UserSerializer(data=charge_chargement_data)
            if charge_chargement_serializer.is_valid():
                charge_chargement = charge_chargement_serializer.save()
                request.data['charge_chargement'] = charge_chargement.id
            else:
                return Response(charge_chargement_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested charge_reception 
        charge_reception_data = request.data.get('charge_reception')
        if isinstance(charge_reception_data, int):
            request.data['charge_reception'] = charge_reception_data
        elif charge_reception_data:
            charge_reception_serializer = UserSerializer(data=charge_reception_data)
            if charge_reception_serializer.is_valid():
                charge_reception = charge_reception_serializer.save()
                request.data['charge_reception'] = charge_reception.id
            else:
                return Response(charge_reception_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        bulletinsescort_serializer = self.get_serializer(data=request.data)
        bulletinsescort_serializer.is_valid(raise_exception=True)
        bulletinsescort_instance = bulletinsescort_serializer.save()


        headers = self.get_success_headers(bulletinsescort_serializer.data)
        return Response(bulletinsescort_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested gros
        gros_data = request.data.pop('gros', None)
        if isinstance(gros_data, int):
            request.data['gros'] = gros_data
        elif gros_data:
            gros_id = gros_data.get('id')
            if gros_id:
                # If 'id' is present, it's an update
                gros_instance = Gros.objects.get(id=gros_id)
                gros_serializer = GrosSerializer(gros_instance,data=gros_data, partial=partial)
                gros_serializer.is_valid(raise_exception=True)
                gros_serializer.save()
            else:
                # If 'id' is not present, it's a create
                gros_serializer = GrosSerializer(data=gros_data)
                gros_serializer.is_valid(raise_exception=True)
                gros = gros_serializer.save()
                request.data['gros'] = gros.id


        # Update nested charge_chargement
        charge_chargement_data = request.data.pop('charge_chargement', None)
        if isinstance(charge_chargement_data, int):
            request.data['charge_chargement'] = charge_chargement_data
        elif charge_chargement_data:
            charge_chargement_id = charge_chargement_data.get('id')
            if charge_chargement_id:
                # If 'id' is present, it's an update
                charge_chargement_instance = User.objects.get(id=charge_chargement_id)
                charge_chargement_serializer = UserSerializer(charge_chargement_instance,data=charge_chargement_data, partial=partial)
                charge_chargement_serializer.is_valid(raise_exception=True)
                charge_chargement_serializer.save()
            else:
                # If 'id' is not present, it's a create
                charge_chargement_serializer = UserSerializer(data=charge_chargement_data)
                charge_chargement_serializer.is_valid(raise_exception=True)
                charge_chargement = charge_chargement_serializer.save()
                request.data['charge_chargement'] = charge_chargement.id


        # Update nested charge_reception
        charge_reception_data = request.data.pop('charge_reception', None)
        if isinstance(charge_reception_data, int):
            request.data['charge_reception'] = charge_reception_data
        elif charge_reception_data:
            charge_reception_id = charge_reception_data.get('id')
            if charge_reception_id:
                # If 'id' is present, it's an update
                charge_reception_instance = User.objects.get(id=charge_reception_id)
                charge_reception_serializer = UserSerializer(charge_reception_instance,data=charge_reception_data, partial=partial)
                charge_reception_serializer.is_valid(raise_exception=True)
                charge_reception_serializer.save()
            else:
                # If 'id' is not present, it's a create
                charge_reception_serializer = UserSerializer(data=charge_reception_data)
                charge_reception_serializer.is_valid(raise_exception=True)
                charge_reception = charge_reception_serializer.save()
                request.data['charge_reception'] = charge_reception.id


        bulletinsescort_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        bulletinsescort_serializer.is_valid(raise_exception=True)
        bulletinsescort_instance = bulletinsescort_serializer.save()


        return Response(bulletinsescort_serializer.data)


    def get_queryset(self):
        queryset = BulletinsEscort.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'charge_chargement'):
            queryset = queryset.prefetch_related('charge_chargement')
        if is_expanded(self.request, 'charge_reception'):
            queryset = queryset.prefetch_related('charge_reception')
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


class TcViewSet(viewsets.ModelViewSet):
    queryset = Tc.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = TcSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= TcFilter


    def create(self, request, *args, **kwargs):
        # Create nested article 
        article_data = request.data.get('article')
        if isinstance(article_data, int):
            request.data['article'] = article_data
        elif article_data:
            article_serializer = ArticleSerializer(data=article_data)
            if article_serializer.is_valid():
                article = article_serializer.save()
                request.data['article'] = article.id
            else:
                return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested type_tc 
        type_tc_data = request.data.get('type_tc')
        if isinstance(type_tc_data, int):
            request.data['type_tc'] = type_tc_data
        elif type_tc_data:
            type_tc_serializer = TypeSerializer(data=type_tc_data)
            if type_tc_serializer.is_valid():
                type_tc = type_tc_serializer.save()
                request.data['type_tc'] = type_tc.id
            else:
                return Response(type_tc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested bulletins 
        bulletins_data = request.data.get('bulletins')
        if isinstance(bulletins_data, int):
            request.data['bulletins'] = bulletins_data
        elif bulletins_data:
            bulletins_serializer = BulletinsEscortSerializer(data=bulletins_data)
            if bulletins_serializer.is_valid():
                bulletins = bulletins_serializer.save()
                request.data['bulletins'] = bulletins.id
            else:
                return Response(bulletins_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested receved_by 
        receved_by_data = request.data.get('receved_by')
        if isinstance(receved_by_data, int):
            request.data['receved_by'] = receved_by_data
        elif receved_by_data:
            receved_by_serializer = UserSerializer(data=receved_by_data)
            if receved_by_serializer.is_valid():
                receved_by = receved_by_serializer.save()
                request.data['receved_by'] = receved_by.id
            else:
                return Response(receved_by_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested current_scelle 
        current_scelle_data = request.data.get('current_scelle')
        if isinstance(current_scelle_data, int):
            request.data['current_scelle'] = current_scelle_data
        elif current_scelle_data:
            current_scelle_serializer = ScelleSerializer(data=current_scelle_data)
            if current_scelle_serializer.is_valid():
                current_scelle = current_scelle_serializer.save()
                request.data['current_scelle'] = current_scelle.id
            else:
                return Response(current_scelle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        tc_serializer = self.get_serializer(data=request.data)
        tc_serializer.is_valid(raise_exception=True)
        tc_instance = tc_serializer.save()


        headers = self.get_success_headers(tc_serializer.data)
        return Response(tc_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested article
        article_data = request.data.pop('article', None)
        if isinstance(article_data, int):
            request.data['article'] = article_data
        elif article_data:
            article_id = article_data.get('id')
            if article_id:
                # If 'id' is present, it's an update
                article_instance = Article.objects.get(id=article_id)
                article_serializer = ArticleSerializer(article_instance,data=article_data, partial=partial)
                article_serializer.is_valid(raise_exception=True)
                article_serializer.save()
            else:
                # If 'id' is not present, it's a create
                article_serializer = ArticleSerializer(data=article_data)
                article_serializer.is_valid(raise_exception=True)
                article = article_serializer.save()
                request.data['article'] = article.id


        # Update nested type_tc
        type_tc_data = request.data.pop('type_tc', None)
        if isinstance(type_tc_data, int):
            request.data['type_tc'] = type_tc_data
        elif type_tc_data:
            type_tc_id = type_tc_data.get('id')
            if type_tc_id:
                # If 'id' is present, it's an update
                type_tc_instance = Type.objects.get(id=type_tc_id)
                type_tc_serializer = TypeSerializer(type_tc_instance,data=type_tc_data, partial=partial)
                type_tc_serializer.is_valid(raise_exception=True)
                type_tc_serializer.save()
            else:
                # If 'id' is not present, it's a create
                type_tc_serializer = TypeSerializer(data=type_tc_data)
                type_tc_serializer.is_valid(raise_exception=True)
                type_tc = type_tc_serializer.save()
                request.data['type_tc'] = type_tc.id


        # Update nested bulletins
        bulletins_data = request.data.pop('bulletins', None)
        if isinstance(bulletins_data, int):
            request.data['bulletins'] = bulletins_data
        elif bulletins_data:
            bulletins_id = bulletins_data.get('id')
            if bulletins_id:
                # If 'id' is present, it's an update
                bulletins_instance = BulletinsEscort.objects.get(id=bulletins_id)
                bulletins_serializer = BulletinsEscortSerializer(bulletins_instance,data=bulletins_data, partial=partial)
                bulletins_serializer.is_valid(raise_exception=True)
                bulletins_serializer.save()
            else:
                # If 'id' is not present, it's a create
                bulletins_serializer = BulletinsEscortSerializer(data=bulletins_data)
                bulletins_serializer.is_valid(raise_exception=True)
                bulletins = bulletins_serializer.save()
                request.data['bulletins'] = bulletins.id


        # Update nested receved_by
        receved_by_data = request.data.pop('receved_by', None)
        if isinstance(receved_by_data, int):
            request.data['receved_by'] = receved_by_data
        elif receved_by_data:
            receved_by_id = receved_by_data.get('id')
            if receved_by_id:
                # If 'id' is present, it's an update
                receved_by_instance = User.objects.get(id=receved_by_id)
                receved_by_serializer = UserSerializer(receved_by_instance,data=receved_by_data, partial=partial)
                receved_by_serializer.is_valid(raise_exception=True)
                receved_by_serializer.save()
            else:
                # If 'id' is not present, it's a create
                receved_by_serializer = UserSerializer(data=receved_by_data)
                receved_by_serializer.is_valid(raise_exception=True)
                receved_by = receved_by_serializer.save()
                request.data['receved_by'] = receved_by.id


        # Update nested current_scelle
        current_scelle_data = request.data.pop('current_scelle', None)
        if isinstance(current_scelle_data, int):
            request.data['current_scelle'] = current_scelle_data
        elif current_scelle_data:
            current_scelle_id = current_scelle_data.get('id')
            if current_scelle_id:
                # If 'id' is present, it's an update
                current_scelle_instance = Scelle.objects.get(id=current_scelle_id)
                current_scelle_serializer = ScelleSerializer(current_scelle_instance,data=current_scelle_data, partial=partial)
                current_scelle_serializer.is_valid(raise_exception=True)
                current_scelle_serializer.save()
            else:
                # If 'id' is not present, it's a create
                current_scelle_serializer = ScelleSerializer(data=current_scelle_data)
                current_scelle_serializer.is_valid(raise_exception=True)
                current_scelle = current_scelle_serializer.save()
                request.data['current_scelle'] = current_scelle.id


        tc_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        tc_serializer.is_valid(raise_exception=True)
        tc_instance = tc_serializer.save()


        return Response(tc_serializer.data)


    def get_queryset(self):
        queryset = Tc.objects.all()
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
        if is_expanded(self.request, 'type_tc'):
            queryset = queryset.prefetch_related('type_tc')
        if is_expanded(self.request, 'bulletins'):
            queryset = queryset.prefetch_related('bulletins')
        if is_expanded(self.request, 'receved_by'):
            queryset = queryset.prefetch_related('receved_by')
        if is_expanded(self.request, 'current_scelle'):
            queryset = queryset.prefetch_related('current_scelle')
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


class SousArticleViewSet(viewsets.ModelViewSet):
    queryset = SousArticle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = SousArticleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= SousArticleFilter


    def create(self, request, *args, **kwargs):
        # Create nested tc 
        tc_data = request.data.get('tc')
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_serializer = TcSerializer(data=tc_data)
            if tc_serializer.is_valid():
                tc = tc_serializer.save()
                request.data['tc'] = tc.id
            else:
                return Response(tc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested client 
        client_data = request.data.get('client')
        if isinstance(client_data, int):
            request.data['client'] = client_data
        elif client_data:
            client_serializer = ClientSerializer(data=client_data)
            if client_serializer.is_valid():
                client = client_serializer.save()
                request.data['client'] = client.id
            else:
                return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested transitaire 
        transitaire_data = request.data.get('transitaire')
        if isinstance(transitaire_data, int):
            request.data['transitaire'] = transitaire_data
        elif transitaire_data:
            transitaire_serializer = TransitaireSerializer(data=transitaire_data)
            if transitaire_serializer.is_valid():
                transitaire = transitaire_serializer.save()
                request.data['transitaire'] = transitaire.id
            else:
                return Response(transitaire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested box 
        box_data = request.data.get('box')
        if isinstance(box_data, int):
            request.data['box'] = box_data
        elif box_data:
            box_serializer = BoxSerializer(data=box_data)
            if box_serializer.is_valid():
                box = box_serializer.save()
                request.data['box'] = box.id
            else:
                return Response(box_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        sousarticle_serializer = self.get_serializer(data=request.data)
        sousarticle_serializer.is_valid(raise_exception=True)
        sousarticle_instance = sousarticle_serializer.save()


        headers = self.get_success_headers(sousarticle_serializer.data)
        return Response(sousarticle_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested tc
        tc_data = request.data.pop('tc', None)
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_id = tc_data.get('id')
            if tc_id:
                # If 'id' is present, it's an update
                tc_instance = Tc.objects.get(id=tc_id)
                tc_serializer = TcSerializer(tc_instance,data=tc_data, partial=partial)
                tc_serializer.is_valid(raise_exception=True)
                tc_serializer.save()
            else:
                # If 'id' is not present, it's a create
                tc_serializer = TcSerializer(data=tc_data)
                tc_serializer.is_valid(raise_exception=True)
                tc = tc_serializer.save()
                request.data['tc'] = tc.id


        # Update nested client
        client_data = request.data.pop('client', None)
        if isinstance(client_data, int):
            request.data['client'] = client_data
        elif client_data:
            client_id = client_data.get('id')
            if client_id:
                # If 'id' is present, it's an update
                client_instance = Client.objects.get(id=client_id)
                client_serializer = ClientSerializer(client_instance,data=client_data, partial=partial)
                client_serializer.is_valid(raise_exception=True)
                client_serializer.save()
            else:
                # If 'id' is not present, it's a create
                client_serializer = ClientSerializer(data=client_data)
                client_serializer.is_valid(raise_exception=True)
                client = client_serializer.save()
                request.data['client'] = client.id


        # Update nested transitaire
        transitaire_data = request.data.pop('transitaire', None)
        if isinstance(transitaire_data, int):
            request.data['transitaire'] = transitaire_data
        elif transitaire_data:
            transitaire_id = transitaire_data.get('id')
            if transitaire_id:
                # If 'id' is present, it's an update
                transitaire_instance = Transitaire.objects.get(id=transitaire_id)
                transitaire_serializer = TransitaireSerializer(transitaire_instance,data=transitaire_data, partial=partial)
                transitaire_serializer.is_valid(raise_exception=True)
                transitaire_serializer.save()
            else:
                # If 'id' is not present, it's a create
                transitaire_serializer = TransitaireSerializer(data=transitaire_data)
                transitaire_serializer.is_valid(raise_exception=True)
                transitaire = transitaire_serializer.save()
                request.data['transitaire'] = transitaire.id


        # Update nested box
        box_data = request.data.pop('box', None)
        if isinstance(box_data, int):
            request.data['box'] = box_data
        elif box_data:
            box_id = box_data.get('id')
            if box_id:
                # If 'id' is present, it's an update
                box_instance = Box.objects.get(id=box_id)
                box_serializer = BoxSerializer(box_instance,data=box_data, partial=partial)
                box_serializer.is_valid(raise_exception=True)
                box_serializer.save()
            else:
                # If 'id' is not present, it's a create
                box_serializer = BoxSerializer(data=box_data)
                box_serializer.is_valid(raise_exception=True)
                box = box_serializer.save()
                request.data['box'] = box.id


        sousarticle_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        sousarticle_serializer.is_valid(raise_exception=True)
        sousarticle_instance = sousarticle_serializer.save()


        return Response(sousarticle_serializer.data)


    def get_queryset(self):
        queryset = SousArticle.objects.all()
        if is_expanded(self.request, 'tc'):
            queryset = queryset.prefetch_related('tc')
        if is_expanded(self.request, 'client'):
            queryset = queryset.prefetch_related('client')
        if is_expanded(self.request, 'transitaire'):
            queryset = queryset.prefetch_related('transitaire')
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


class VisiteViewSet(viewsets.ModelViewSet):
    queryset = Visite.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = VisiteSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= VisiteFilter


    def create(self, request, *args, **kwargs):
        # Create nested gros 
        gros_data = request.data.get('gros')
        if isinstance(gros_data, int):
            request.data['gros'] = gros_data
        elif gros_data:
            gros_serializer = GrosSerializer(data=gros_data)
            if gros_serializer.is_valid():
                gros = gros_serializer.save()
                request.data['gros'] = gros.id
            else:
                return Response(gros_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested article 
        article_data = request.data.get('article')
        if isinstance(article_data, int):
            request.data['article'] = article_data
        elif article_data:
            article_serializer = ArticleSerializer(data=article_data)
            if article_serializer.is_valid():
                article = article_serializer.save()
                request.data['article'] = article.id
            else:
                return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested transitaire 
        transitaire_data = request.data.get('transitaire')
        if isinstance(transitaire_data, int):
            request.data['transitaire'] = transitaire_data
        elif transitaire_data:
            transitaire_serializer = TransitaireSerializer(data=transitaire_data)
            if transitaire_serializer.is_valid():
                transitaire = transitaire_serializer.save()
                request.data['transitaire'] = transitaire.id
            else:
                return Response(transitaire_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        visite_serializer = self.get_serializer(data=request.data)
        visite_serializer.is_valid(raise_exception=True)
        visite_instance = visite_serializer.save()


        headers = self.get_success_headers(visite_serializer.data)
        return Response(visite_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested gros
        gros_data = request.data.pop('gros', None)
        if isinstance(gros_data, int):
            request.data['gros'] = gros_data
        elif gros_data:
            gros_id = gros_data.get('id')
            if gros_id:
                # If 'id' is present, it's an update
                gros_instance = Gros.objects.get(id=gros_id)
                gros_serializer = GrosSerializer(gros_instance,data=gros_data, partial=partial)
                gros_serializer.is_valid(raise_exception=True)
                gros_serializer.save()
            else:
                # If 'id' is not present, it's a create
                gros_serializer = GrosSerializer(data=gros_data)
                gros_serializer.is_valid(raise_exception=True)
                gros = gros_serializer.save()
                request.data['gros'] = gros.id


        # Update nested article
        article_data = request.data.pop('article', None)
        if isinstance(article_data, int):
            request.data['article'] = article_data
        elif article_data:
            article_id = article_data.get('id')
            if article_id:
                # If 'id' is present, it's an update
                article_instance = Article.objects.get(id=article_id)
                article_serializer = ArticleSerializer(article_instance,data=article_data, partial=partial)
                article_serializer.is_valid(raise_exception=True)
                article_serializer.save()
            else:
                # If 'id' is not present, it's a create
                article_serializer = ArticleSerializer(data=article_data)
                article_serializer.is_valid(raise_exception=True)
                article = article_serializer.save()
                request.data['article'] = article.id


        # Update nested transitaire
        transitaire_data = request.data.pop('transitaire', None)
        if isinstance(transitaire_data, int):
            request.data['transitaire'] = transitaire_data
        elif transitaire_data:
            transitaire_id = transitaire_data.get('id')
            if transitaire_id:
                # If 'id' is present, it's an update
                transitaire_instance = Transitaire.objects.get(id=transitaire_id)
                transitaire_serializer = TransitaireSerializer(transitaire_instance,data=transitaire_data, partial=partial)
                transitaire_serializer.is_valid(raise_exception=True)
                transitaire_serializer.save()
            else:
                # If 'id' is not present, it's a create
                transitaire_serializer = TransitaireSerializer(data=transitaire_data)
                transitaire_serializer.is_valid(raise_exception=True)
                transitaire = transitaire_serializer.save()
                request.data['transitaire'] = transitaire.id


        visite_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        visite_serializer.is_valid(raise_exception=True)
        visite_instance = visite_serializer.save()


        return Response(visite_serializer.data)


    def get_queryset(self):
        queryset = Visite.objects.all()
        if is_expanded(self.request, 'gros'):
            queryset = queryset.prefetch_related('gros')
        if is_expanded(self.request, 'article'):
            queryset = queryset.prefetch_related('article')
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


class VisiteItemViewSet(viewsets.ModelViewSet):
    queryset = VisiteItem.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = VisiteItemSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= VisiteItemFilter


    def create(self, request, *args, **kwargs):
        # Create nested visite 
        visite_data = request.data.get('visite')
        if isinstance(visite_data, int):
            request.data['visite'] = visite_data
        elif visite_data:
            visite_serializer = VisiteSerializer(data=visite_data)
            if visite_serializer.is_valid():
                visite = visite_serializer.save()
                request.data['visite'] = visite.id
            else:
                return Response(visite_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # Create nested tc 
        tc_data = request.data.get('tc')
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_serializer = TcSerializer(data=tc_data)
            if tc_serializer.is_valid():
                tc = tc_serializer.save()
                request.data['tc'] = tc.id
            else:
                return Response(tc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        visiteitem_serializer = self.get_serializer(data=request.data)
        visiteitem_serializer.is_valid(raise_exception=True)
        visiteitem_instance = visiteitem_serializer.save()


        headers = self.get_success_headers(visiteitem_serializer.data)
        return Response(visiteitem_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested visite
        visite_data = request.data.pop('visite', None)
        if isinstance(visite_data, int):
            request.data['visite'] = visite_data
        elif visite_data:
            visite_id = visite_data.get('id')
            if visite_id:
                # If 'id' is present, it's an update
                visite_instance = Visite.objects.get(id=visite_id)
                visite_serializer = VisiteSerializer(visite_instance,data=visite_data, partial=partial)
                visite_serializer.is_valid(raise_exception=True)
                visite_serializer.save()
            else:
                # If 'id' is not present, it's a create
                visite_serializer = VisiteSerializer(data=visite_data)
                visite_serializer.is_valid(raise_exception=True)
                visite = visite_serializer.save()
                request.data['visite'] = visite.id


        # Update nested tc
        tc_data = request.data.pop('tc', None)
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_id = tc_data.get('id')
            if tc_id:
                # If 'id' is present, it's an update
                tc_instance = Tc.objects.get(id=tc_id)
                tc_serializer = TcSerializer(tc_instance,data=tc_data, partial=partial)
                tc_serializer.is_valid(raise_exception=True)
                tc_serializer.save()
            else:
                # If 'id' is not present, it's a create
                tc_serializer = TcSerializer(data=tc_data)
                tc_serializer.is_valid(raise_exception=True)
                tc = tc_serializer.save()
                request.data['tc'] = tc.id


        visiteitem_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        visiteitem_serializer.is_valid(raise_exception=True)
        visiteitem_instance = visiteitem_serializer.save()


        return Response(visiteitem_serializer.data)


    def get_queryset(self):
        queryset = VisiteItem.objects.all()
        if is_expanded(self.request, 'visite'):
            queryset = queryset.prefetch_related('visite')
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


class ScelleViewSet(viewsets.ModelViewSet):
    queryset = Scelle.objects.all()
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    serializer_class = ScelleSerializer
    pagination_class = CustomPagination
    ordering_fields = '__all__'
    filterset_class= ScelleFilter


    def create(self, request, *args, **kwargs):
        Scelle_data = request.data.pop('Scelle',[])
        # Create nested tc 
        tc_data = request.data.get('tc')
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_serializer = TcSerializer(data=tc_data)
            if tc_serializer.is_valid():
                tc = tc_serializer.save()
                request.data['tc'] = tc.id
            else:
                return Response(tc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        scelle_serializer = self.get_serializer(data=request.data)
        scelle_serializer.is_valid(raise_exception=True)
        scelle_instance = scelle_serializer.save()


        # Create nested Scelle


        for tc_data in Scelle_data:
            tc_data['scelle'] = scelle_instance.id
            tc_serializer = TcSerializer(data=tc_data)
            tc_serializer.is_valid(raise_exception=True)
            tc_serializer.save()


        headers = self.get_success_headers(scelle_serializer.data)
        return Response(scelle_serializer.data, status=201, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        # Update nested tc
        tc_data = request.data.pop('tc', None)
        if isinstance(tc_data, int):
            request.data['tc'] = tc_data
        elif tc_data:
            tc_id = tc_data.get('id')
            if tc_id:
                # If 'id' is present, it's an update
                tc_instance = Tc.objects.get(id=tc_id)
                tc_serializer = TcSerializer(tc_instance,data=tc_data, partial=partial)
                tc_serializer.is_valid(raise_exception=True)
                tc_serializer.save()
            else:
                # If 'id' is not present, it's a create
                tc_serializer = TcSerializer(data=tc_data)
                tc_serializer.is_valid(raise_exception=True)
                tc = tc_serializer.save()
                request.data['tc'] = tc.id


        scelle_serializer = self.get_serializer(instance,data=request.data, partial=partial)
        scelle_serializer.is_valid(raise_exception=True)
        scelle_instance = scelle_serializer.save()


        # Update nested Scelle 
        Scelle_data = request.data.pop('Scelle', [])
        if Scelle_data:
            for tc_data in Scelle_data:
                if isinstance(tc_data, int):
                    pass
                else: 
                    tc_id = Scelle_data.get('id')
                    if tc_id:
                        # If 'id' is present, it's an update
                        Scelle_instance = Tc.objects.get(id=tc_id)
                        Scelle_serializer = TcSerializer(Scelle_instance, data=Scelle_data, partial=partial)
                    else:
                        # If 'id' is not present, it's a create
                        Scelle_data['scelle'] = scelle_instance.id
                        Scelle_serializer = TcSerializer(data=Scelle_data)
                    Scelle_serializer.is_valid(raise_exception=True)
                    Scelle_serializer.save()
        return Response(scelle_serializer.data)


    def get_queryset(self):
        queryset = Scelle.objects.all()
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


