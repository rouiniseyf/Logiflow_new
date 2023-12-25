from rest_framework import routers
from django.urls import path, include
from .views import *
app_name='billing'


router = routers.DefaultRouter()


urlpatterns = []


router.register(r'proforma', ProformaViewSet, basename='proforma')
router.register(r'groupe', GroupeViewSet, basename='groupe')
router.register(r'groupeligne', GroupeLigneViewSet, basename='groupeligne')
router.register(r'ligneprestation', LignePrestationViewSet, basename='ligneprestation')
router.register(r'ligneprestationarticle', LignePrestationArticleViewSet, basename='ligneprestationarticle')
router.register(r'boncommande', BonCommandeViewSet, basename='boncommande')
router.register(r'commande', CommandeViewSet, basename='commande')
router.register(r'facture', FactureViewSet, basename='facture')
router.register(r'paiement', PaiementViewSet, basename='paiement')
router.register(r'facturecomplementaire', FactureComplementaireViewSet, basename='facturecomplementaire')
router.register(r'lignefacturecomplementaire', LigneFactureComplementaireViewSet, basename='lignefacturecomplementaire')
router.register(r'paiementfacturecomplementaire', PaiementFactureComplementaireViewSet, basename='paiementfacturecomplementaire')
router.register(r'factureavoire', FactureAvoireViewSet, basename='factureavoire')
router.register(r'lignefactureavoire', LigneFactureAvoireViewSet, basename='lignefactureavoire')
router.register(r'bonsortie', BonSortieViewSet, basename='bonsortie')
router.register(r'bonsortieitem', BonSortieItemViewSet, basename='bonsortieitem')
router.register(r'facturelibre', FactureLibreViewSet, basename='facturelibre')
router.register(r'lignefacturelibre', LigneFactureLibreViewSet, basename='lignefacturelibre')
router.register(r'paiementfacturelibre', PaiementFactureLibreViewSet, basename='paiementfacturelibre')
router.register(r'proformagroupage', ProformaGroupageViewSet, basename='proformagroupage')
router.register(r'ligneproformagroupage', LigneProformaGroupageViewSet, basename='ligneproformagroupage')
router.register(r'facturegroupage', FactureGroupageViewSet, basename='facturegroupage')
router.register(r'paiementgroupage', PaiementGroupageViewSet, basename='paiementgroupage')
router.register(r'bonsortiegroupage', BonSortieGroupageViewSet, basename='bonsortiegroupage')
urlpatterns += router.urls
