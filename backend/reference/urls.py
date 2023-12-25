from rest_framework import routers
from .views import *
from django.urls import path, include

app_name='reference'


router = routers.DefaultRouter()


urlpatterns = []


router.register(r'pays', PaysViewSet, basename='pays')
router.register(r'port', PortViewSet, basename='port')
router.register(r'type', TypeViewSet, basename='type')
router.register(r'transitaire', TransitaireViewSet, basename='transitaire')
router.register(r'groupeur', GroupeurViewSet, basename='groupeur')
router.register(r'navire', NavireViewSet, basename='navire')
router.register(r'armateur', ArmateurViewSet, basename='armateur')
router.register(r'consignataire', ConsignataireViewSet, basename='consignataire')
router.register(r'agent', AgentViewSet, basename='agent')
router.register(r'client', ClientViewSet, basename='client')
router.register(r'parc', ParcViewSet, basename='parc')
router.register(r'box', BoxViewSet, basename='box')
router.register(r'zone', ZoneViewSet, basename='zone')
router.register(r'banque', BanqueViewSet, basename='banque')
router.register(r'direction', DirectionViewSet, basename='direction')
urlpatterns += router.urls
