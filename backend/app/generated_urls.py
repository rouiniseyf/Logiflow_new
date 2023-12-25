from rest_framework import routers
from .views import *
app_name='app'


router = routers.DefaultRouter()


urlpatterns = []


router.register(r'gros', GrosViewSet, basename='gros')
router.register(r'article', ArticleViewSet, basename='article')
router.register(r'position', PositionViewSet, basename='position')
router.register(r'bulletinsescort', BulletinsEscortViewSet, basename='bulletinsescort')
router.register(r'tc', TcViewSet, basename='tc')
router.register(r'sousarticle', SousArticleViewSet, basename='sousarticle')
router.register(r'visite', VisiteViewSet, basename='visite')
router.register(r'visiteitem', VisiteItemViewSet, basename='visiteitem')
router.register(r'scelle', ScelleViewSet, basename='scelle')
urlpatterns += router.urls
