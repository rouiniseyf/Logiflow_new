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


def printFilters(): 
    filter_set_instance  = GrosFilter()

    # Access the filters and print them
    for name, filter_instance in filter_set_instance.filters.items():
        print(f"Filter Name: {name}")
        print(f"Filter Class: {filter_instance.__class__.__name__}")
        
        # Check if lookup_exprs attribute is available before trying to access it
        if hasattr(filter_instance.field, 'lookup_exprs'):
            print(f"Filter Lookup Types: {filter_instance.field.lookup_exprs}")
        else:
            print("Filter Lookup Types: N/A")

        print("--------------")