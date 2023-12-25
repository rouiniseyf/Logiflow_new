from .models import *
from .serializers import *
from src.utils import generate_filter_set 


BaremeFilter = generate_filter_set(Bareme)
RegimeFilter = generate_filter_set(Regime)
RubriqueFilter = generate_filter_set(Rubrique)
PrestationFilter = generate_filter_set(Prestation)
PrestationOccasionnelleFilter = generate_filter_set(PrestationOccasionnelle)
PrestationOccasionnelleGroupageFilter = generate_filter_set(PrestationOccasionnelleGroupage)
PrestationArticleFilter = generate_filter_set(PrestationArticle)
SejourFilter = generate_filter_set(Sejour)
SejourTcGroupageFilter = generate_filter_set(SejourTcGroupage)
SejourSousArticleGroupageFilter = generate_filter_set(SejourSousArticleGroupage)
BranchementFilter = generate_filter_set(Branchement)
PrestationGroupageFilter = generate_filter_set(PrestationGroupage)
PrestationVisiteGroupageFilter = generate_filter_set(PrestationVisiteGroupage)
