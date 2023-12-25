from .models import *
from .serializers import *
from src.utils import generate_filter_set 


VisiteGroupageFilter = generate_filter_set(VisiteGroupage)
PositionGroupageFilter = generate_filter_set(PositionGroupage)
