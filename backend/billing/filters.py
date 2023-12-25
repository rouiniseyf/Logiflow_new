from .models import *
from .serializers import *
from src.utils import generate_filter_set 


ProformaFilter = generate_filter_set(Proforma)
GroupeFilter = generate_filter_set(Groupe)
GroupeLigneFilter = generate_filter_set(GroupeLigne)
LignePrestationFilter = generate_filter_set(LignePrestation)
LignePrestationArticleFilter = generate_filter_set(LignePrestationArticle)
BonCommandeFilter = generate_filter_set(BonCommande)
CommandeFilter = generate_filter_set(Commande)
FactureFilter = generate_filter_set(Facture)
PaiementFilter = generate_filter_set(Paiement)
FactureComplementaireFilter = generate_filter_set(FactureComplementaire)
LigneFactureComplementaireFilter = generate_filter_set(LigneFactureComplementaire)
PaiementFactureComplementaireFilter = generate_filter_set(PaiementFactureComplementaire)
FactureAvoireFilter = generate_filter_set(FactureAvoire)
LigneFactureAvoireFilter = generate_filter_set(LigneFactureAvoire)
BonSortieFilter = generate_filter_set(BonSortie)
BonSortieItemFilter = generate_filter_set(BonSortieItem)
FactureLibreFilter = generate_filter_set(FactureLibre)
LigneFactureLibreFilter = generate_filter_set(LigneFactureLibre)
PaiementFactureLibreFilter = generate_filter_set(PaiementFactureLibre)
ProformaGroupageFilter = generate_filter_set(ProformaGroupage)
LigneProformaGroupageFilter = generate_filter_set(LigneProformaGroupage)
FactureGroupageFilter = generate_filter_set(FactureGroupage)
PaiementGroupageFilter = generate_filter_set(PaiementGroupage)
BonSortieGroupageFilter = generate_filter_set(BonSortieGroupage)
