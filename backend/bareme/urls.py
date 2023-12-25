from rest_framework import routers
from .views import *
from django.urls import path, include


app_name='bareme'


router = routers.DefaultRouter()


urlpatterns = []


router.register(r'bareme', BaremeViewSet, basename='bareme')
router.register(r'regime', RegimeViewSet, basename='regime')
router.register(r'rubrique', RubriqueViewSet, basename='rubrique')
router.register(r'prestation', PrestationViewSet, basename='prestation')
router.register(r'prestationoccasionnelle', PrestationOccasionnelleViewSet, basename='prestationoccasionnelle')
router.register(r'prestationoccasionnellegroupage', PrestationOccasionnelleGroupageViewSet, basename='prestationoccasionnellegroupage')
router.register(r'prestationarticle', PrestationArticleViewSet, basename='prestationarticle')
router.register(r'sejour', SejourViewSet, basename='sejour')
router.register(r'sejourtcgroupage', SejourTcGroupageViewSet, basename='sejourtcgroupage')
router.register(r'sejoursousarticlegroupage', SejourSousArticleGroupageViewSet, basename='sejoursousarticlegroupage')
router.register(r'branchement', BranchementViewSet, basename='branchement')
router.register(r'prestationgroupage', PrestationGroupageViewSet, basename='prestationgroupage')
router.register(r'prestationvisitegroupage', PrestationVisiteGroupageViewSet, basename='prestationvisitegroupage')
urlpatterns += router.urls
