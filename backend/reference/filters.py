from .models import *
from .serializers import *
from src.utils import generate_filter_set 


PaysFilter = generate_filter_set(Pays)
PortFilter = generate_filter_set(Port)
TypeFilter = generate_filter_set(Type)
TransitaireFilter = generate_filter_set(Transitaire)
GroupeurFilter = generate_filter_set(Groupeur)
NavireFilter = generate_filter_set(Navire)
ArmateurFilter = generate_filter_set(Armateur)
ConsignataireFilter = generate_filter_set(Consignataire)
AgentFilter = generate_filter_set(Agent)
ClientFilter = generate_filter_set(Client)
ParcFilter = generate_filter_set(Parc)
BoxFilter = generate_filter_set(Box)
ZoneFilter = generate_filter_set(Zone)
BanqueFilter = generate_filter_set(Banque)
DirectionFilter = generate_filter_set(Direction)
