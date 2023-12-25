from rest_framework import routers
from .views import *
app_name='reporting'


router = routers.DefaultRouter()


urlpatterns = []


urlpatterns += router.urls
