from rest_framework import routers
from .views import *
from django.urls import path, include


app_name='groupage'


router = routers.DefaultRouter()


urlpatterns = [
  
]


router.register(r'visitegroupage', VisiteGroupageViewSet, basename='visitegroupage')
router.register(r'positiongroupage', PositionGroupageViewSet, basename='positiongroupage')
urlpatterns += router.urls
