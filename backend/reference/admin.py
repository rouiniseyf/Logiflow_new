from django.contrib import admin
from .models import *

#---| Pays |----------------------------------------------------------------------------------------------------------------------


class PaysAdmin(admin.ModelAdmin):

    search_fields = ['code', 'alpha2','alpha3','nom_fr_fr','nom_en_gb',]
    list_display = ['id','code', 'alpha2','alpha3','nom_fr_fr','nom_en_gb',]
    list_display_links = ['id']

admin.site.register(Pays, PaysAdmin)

#---| Port |----------------------------------------------------------------------------------------------------------------------


class PortAdmin(admin.ModelAdmin):

    search_fields = ['raison_sociale', 'code','pays__nom_fr_fr']
    list_display = ['id','raison_sociale', 'code','pays',]
    list_display_links = ['raison_sociale']

admin.site.register(Port, PortAdmin)

#---| Navire |--------------------------------------------------------------------------------------------------------------------


class NavireAdmin(admin.ModelAdmin):

    search_fields = ['nom', 'code',]
    list_display = ['id','nom', 'code',]
    list_display_links = ['nom']

admin.site.register(Navire, NavireAdmin)

#---| Armateur |------------------------------------------------------------------------------------------------------------------


class ArmateurAdmin(admin.ModelAdmin):
    search_fields = ['raison_sociale', 'code',]
    list_display = ['id','raison_sociale', 'code',]
    list_display_links = ['raison_sociale']

admin.site.register(Armateur, ArmateurAdmin)

#---| Consignatire |------------------------------------------------------------------------------------------------------------


class ConsignataireAdmin(admin.ModelAdmin):

    search_fields = ['raison_sociale', ]
    list_display = ['id','raison_sociale', ]
    list_display_links = ['raison_sociale']

admin.site.register(Consignataire, ConsignataireAdmin)

#---| Client |-------------------------------------------------------------------------------------------------------------------


class ClientAdmin(admin.ModelAdmin):
    search_fields = ['raison_sociale', ]
    list_display = ['id','raison_sociale','adress','email','tel','RC','NIF','AI','NIS' ]
    list_display_links = ['raison_sociale']

admin.site.register(Client, ClientAdmin)


#---| Groupeur |----------------------------------------------------------------------------------------------------------------

class GroupeurAdmin(admin.ModelAdmin):
    search_fields = ['raison_sociale', ]
    list_display = ['id','raison_sociale','adress','email','tel', ]
    list_display_links = ['raison_sociale']

admin.site.register(Groupeur, GroupeurAdmin)

#---| Transitaire |---------------------------------------------------------------------------------------------------------------


class TransitaireAdmin(admin.ModelAdmin):
    search_fields = ['raison_sociale', ]
    list_display = ['id','raison_sociale','adress','email','tel', ]
    list_display_links = ['raison_sociale']

admin.site.register(Transitaire, TransitaireAdmin)

#---| Agnet |---------------------------------------------------------------------------------------------------------------------




class AgentAdmin(admin.ModelAdmin):
    search_fields = ['nom','prenom', ]
    list_display = ['id','nom','prenom', ]
    list_display_links = ['id']

admin.site.register(Agent, AgentAdmin)


#---| Type |---------------------------------------------------------------------------------------------------------------------


class TypeAdmin(admin.ModelAdmin):

    search_fields = ['designation', ]
    list_display = ['id','designation', ]
    list_display_links = ['designation']

admin.site.register(Type, TypeAdmin)

#---| Parc |---------------------------------------------------------------------------------------------------------------------

class ParcAdmin(admin.ModelAdmin):
  
    search_fields = ['designation', ]
    list_display = ['id','designation',]
    list_display_links = ['designation']

admin.site.register(Parc, ParcAdmin)


#---| Zone |---------------------------------------------------------------------------------------------------------------------

class ZoneAdmin(admin.ModelAdmin):
    search_fields = ['zone', ]
    list_display = ['id','zone','lignes','ranges' ,'gerbage']
    list_display_links = ['zone']

admin.site.register(Zone, ZoneAdmin)

#---| Banque |---------------------------------------------------------------------------------------------------------------------

class BanqueAdmin(admin.ModelAdmin):
    search_fields = ['raison_sociale', ]
    list_display = ['id','raison_sociale','adress','email','tel',]
    list_display_links = ['raison_sociale']

admin.site.register(Banque, BanqueAdmin)

#---| Banque |---------------------------------------------------------------------------------------------------------------------

class BoxAdmin(admin.ModelAdmin):
    search_fields = ['designation', ]
    list_display = ['id','designation','parc',]
    list_display_links = ['designation']

admin.site.register(Box, BoxAdmin)

#---| Direction |---------------------------------------------------------------------------------------------------------------------

class DirectionAdmin(admin.ModelAdmin):
    search_fields = ['nom', ]
    list_display = ['nom','code','couleur']
    list_display_links = ['nom']

admin.site.register(Direction, DirectionAdmin)

