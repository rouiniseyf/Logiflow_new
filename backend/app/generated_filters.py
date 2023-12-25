from .models import *
from .serializers import *
from src.utils import generate_filter_set 


GrosFilter = generate_filter_set(Gros)
ArticleFilter = generate_filter_set(Article)
PositionFilter = generate_filter_set(Position)
BulletinsEscortFilter = generate_filter_set(BulletinsEscort)
TcFilter = generate_filter_set(Tc)
SousArticleFilter = generate_filter_set(SousArticle)
VisiteFilter = generate_filter_set(Visite)
VisiteItemFilter = generate_filter_set(VisiteItem)
ScelleFilter = generate_filter_set(Scelle)
