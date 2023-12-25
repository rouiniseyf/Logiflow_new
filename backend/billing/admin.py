from django.contrib import admin
from bareme.models import Prestation

from reference.models import Banque 
from .models import *



# list_filter = ['bareme',('accostage', DateRangeFilter),('navire', RelatedDropdownFilter),('armateur', RelatedDropdownFilter),('consignataire', RelatedDropdownFilter)]

# Register your models here.
#---| Proforma |---------------------------------------------------------------------------------------------------------------------

class ProformaAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','numero','date_creation','gros','entreposage','article','TR','HT','TVA','TTC' ]
    list_display_links = ['numero']

    
admin.site.register(Proforma, ProformaAdmin)


#---| Proforma Groupage |---------------------------------------------------------------------------------------------------------------------

class ProformaGroupageAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','numero','date_creation','gros','article','TR','HT','TVA','TTC' ]
    list_display_links = ['numero']
  
admin.site.register(ProformaGroupage, ProformaGroupageAdmin)

#---| Facture |---------------------------------------------------------------------------------------------------------------------


class FactureAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','get_article','numero','date_creation','proforma','HT','TVA','timber','TTC','paid','a_terme','get_client' ]
    list_display_links = ['numero']


    @admin.display( description='CLIENT',)
    def get_client(self, obj):
        return obj.proforma.article.client

    @admin.display( description='ARTICLE',)
    def get_article(self, obj): 
        return obj.proforma.article 

    def delete_queryset(self, request, queryset):     
        for facture in queryset: 
            ids = GroupeLigne.objects.filter(groupe__proforma__id = facture.proforma.id ).values_list("tc__id")

            for id in ids: 
                idd = int(id[-1])
                Tc.objects.get(id=idd).set_as_not_billed()
                
            Proforma.objects.filter(id=facture.proforma.id).delete()
        queryset.delete()
        
admin.site.register(Facture, FactureAdmin)

#---| Facture Libre |---------------------------------------------------------------------------------------------------------------------


class FactureLibreAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','numero','date_creation','date_facture','HT','TVA','timber','TTC' ]
    list_display_links = ['numero']



admin.site.register(FactureLibre, FactureLibreAdmin)


#---| Groupe |---------------------------------------------------------------------------------------------------------------------

class GroupeAdmin(admin.ModelAdmin):
    search_fields = ['proforma','type','dangereux','frigo',]
    list_display = ['id','proforma','type','dangereux','frigo','tcs']
    list_display_links = ['id']

admin.site.register(Groupe, GroupeAdmin)


#---| Groupe Ligne |---------------------------------------------------------------------------------------------------------------------


class GroupeLigneAdmin(admin.ModelAdmin):
    search_fields = ['groupe','tc',]
    list_display = ['id','groupe','tc',]
    list_display_links = ['id']
    list_filter = ['groupe',]

admin.site.register(GroupeLigne, GroupeLigneAdmin)

#---| Bon de Commande |---------------------------------------------------------------------------------------------------------------------

class BonCommandeAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','numero','article','date_creation',]
    list_display_links = ['numero']


    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.tc.article
    
admin.site.register(BonCommande, BonCommandeAdmin)

#---| Commande |---------------------------------------------------------------------------------------------------------------------

class CommandeAdmin(admin.ModelAdmin):
    search_fields = ['tc__tc']
    list_display = ['id','bon_commande','get_article','tc','type','quantite','observation']
    list_display_links = ['id']


    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.tc.article
    
admin.site.register(Commande, CommandeAdmin)




#---| Ligne Prestation |---------------------------------------------------------------------------------------------------------------------


class LignePrestationAdmin(admin.ModelAdmin):
    search_fields = ['rubrique',]
    list_display = ['id','proforma','groupe','rubrique','tcs','quantite','tarif','HT','TVA','TTC']
    list_display_links = ['id']


admin.site.register(LignePrestation, LignePrestationAdmin)


#---| Ligne Prestation Groupage |---------------------------------------------------------------------------------------------------------------------



class LigneProformaGroupageAdmin(admin.ModelAdmin):
    search_fields = ['rubrique',]
    list_display = ['id','proforma','quantite','tarif','HT','TVA','TTC']
    list_display_links = ['id']

admin.site.register(LigneProformaGroupage, LigneProformaGroupageAdmin)

#---| Ligne Facture Libre |---------------------------------------------------------------------------------------------------------------------



class LigneFactureLibreAdmin(admin.ModelAdmin):
    search_fields = ['rubrique',]
    list_display = ['id','facture_libre','tarif','quantite','HT','TVA','TTC']
    list_display_links = ['facture_libre']

admin.site.register(LigneFactureLibre, LigneFactureLibreAdmin)


#---| Ligne Prestation Article|---------------------------------------------------------------------------------------------------------------------



class LignePrestationArticleAdmin(admin.ModelAdmin):
    search_fields = ['rubrique',]
    list_display = ['id','proforma','tarif','HT','TVA','TTC']
    list_display_links = ['id']


admin.site.register(LignePrestationArticle, LignePrestationArticleAdmin)


#---| Paiement |---------------------------------------------------------------------------------------------------------------------



class PaiementAdmin(admin.ModelAdmin):
    search_fields = ['cheque',]
    list_display = ['id','get_article','facture','get_article','get_client','date','mode','banque','cheque','montant',]
    list_display_links = ['id']

    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.facture.proforma.article

    @admin.display( description='CLIENT',)
    def get_client(self, obj):
        return obj.facture.proforma.article.client

    def delete_queryset(self, request, queryset):    
        factures = []  
        for paiement in queryset : 
            factures.append(paiement.facture)
        queryset.delete()

        for facture in factures: 
            facture.refrech_status() 


        
admin.site.register(Paiement, PaiementAdmin)

#---| Paiement |---------------------------------------------------------------------------------------------------------------------



class PaiementFactureLibreAdmin(admin.ModelAdmin):
    search_fields = ['cheque',]
    list_display = ['id','date','mode','banque','cheque','montant',]
    list_display_links = ['id']


admin.site.register(PaiementFactureLibre, PaiementFactureLibreAdmin)


#---| Facture Complimentaire |---------------------------------------------------------------------------------------------------------------------


class FactureComplementaireAdmin(admin.ModelAdmin):
    search_fields = ['facture','numero','date_creation',]
    list_display = ['id','facture','full_number','date_creation','HT','TVA','timber','TTC','paid' ]
    list_display_links = ['full_number','id']

admin.site.register(FactureComplementaire, FactureComplementaireAdmin)

#---| Facture Complimentaire |---------------------------------------------------------------------------------------------------------------------


class FactureAvoireAdmin(admin.ModelAdmin):
    search_fields = ['facture','numero','date_creation',]
    list_display = ['id','facture','numero','date_creation','HT','TVA','TTC' ]
    list_display_links = ['numero']

admin.site.register(FactureAvoire, FactureAvoireAdmin)


#---| Ligne Facture Complimentaire |---------------------------------------------------------------------------------------------------------------------


class LigneFactureComplementaireAdmin(admin.ModelAdmin):
    search_fields = ['facture_complementaire',]
    list_display = ['id','facture_complementaire','rubrique','date','tarif','quantite','HT','TVA','TTC' ]
    list_display_links = ['facture_complementaire']

admin.site.register(LigneFactureComplementaire, LigneFactureComplementaireAdmin)


#---| Ligne Facture Avoire |---------------------------------------------------------------------------------------------------------------------


class LigneFactureAvoireAdmin(admin.ModelAdmin):
    search_fields = ['facture_avoire',]
    list_display = ['id','facture_avoire','rubrique','date','tarif','quantite','HT','TVA','TTC' ]
    list_display_links = ['facture_avoire']

admin.site.register(LigneFactureAvoire, LigneFactureAvoireAdmin)


#---| Paiement |---------------------------------------------------------------------------------------------------------------------



class PaiementFactureComplementaireAdmin(admin.ModelAdmin):
    search_fields = ['cheque',]
    list_display = ['id','date','mode','banque','cheque','montant',]
    list_display_links = ['id']

    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.facture.proforma.article
admin.site.register(PaiementFactureComplementaire, PaiementFactureComplementaireAdmin)



#---| Bon Sortie |---------------------------------------------------------------------------------------------------------------------



class BonSortieAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','numero','get_article','date_sortie','date_creation','facture','d10','badge',]
    list_display_links = ['id']

    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.facture.proforma.article
    
admin.site.register(BonSortie, BonSortieAdmin)


#---| Bon Sortie Item |---------------------------------------------------------------------------------------------------------------------


class BonSortieItemAdmin(admin.ModelAdmin):
    search_fields = ['tc__tc',]
    list_display = ['id','bon_sortie','get_article','tc','matricule']
    list_display_links = ['id']

    @admin.display(description="Article")
    def get_article(self,obj): 
        return obj.tc.article
    

admin.site.register(BonSortieItem, BonSortieItemAdmin)


#---| Facture Groupage |---------------------------------------------------------------------------------------------------------------------


 
class FactureGroupageAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','numero','date_creation','HT','TTC','paid','a_terme' ]
    list_display_links = ['numero']


    @admin.display( description='CLIENT',)
    def get_client(self, obj):
        return obj.proforma.sous_article.client


admin.site.register(FactureGroupage, FactureGroupageAdmin)

#---| Paiement Groupage |---------------------------------------------------------------------------------------------------------------------



class PaiementGroupageAdmin(admin.ModelAdmin):
    search_fields = ['cheque',]
    list_display = ['id','facture','get_article','get_client','date','mode','get_banque','cheque','montant',]
    list_display_links = ['id']

    
    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.facture.proforma.article
    
    @admin.display( description='CLIENT',)
    def get_client(self, obj):
        return obj.facture.proforma.article.client

    @admin.display( description='BANQUE',)
    def get_banque(self, obj):
        return obj.banque.raison_sociale

admin.site.register(PaiementGroupage, PaiementGroupageAdmin)

#---| Bon Sortie Groupage|---------------------------------------------------------------------------------------------------------------------



class BonSortieGroupageAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ['id','numero','get_article','sous_article','date_sortie','date_creation','facture','d10','badge',]
    list_display_links = ['id']

    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.facture.proforma.article
    
admin.site.register(BonSortieGroupage, BonSortieGroupageAdmin)
