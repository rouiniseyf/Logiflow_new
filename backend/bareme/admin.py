from django.contrib import admin
from .models import *


#---| Bareme |---------------------------------------------------------------------------------------------------------------------

class BaremeAdmin(admin.ModelAdmin):
    search_fields = ['designation','starting_date','ending_date', ]
    list_display = ['id','designation','starting_date','ending_date','accostage' ]
    list_display_links = ['designation']

admin.site.register(Bareme, BaremeAdmin)

#---| Regime |-----------------------------------------------------------------------------------------------------------------------



class RegimeAdmin(admin.ModelAdmin):
    search_fields = ['designation',  ]
    list_display = ['id','designation','bareme','parc']
    list_display_links = ['designation']

admin.site.register(Regime, RegimeAdmin)

#---| Rubrique |---------------------------------------------------------------------------------------------------------------------

class RubriqueAdmin(admin.ModelAdmin):
    search_fields = ['code','designation' ]
    list_display = ['id','designation','type_calcule','code','appliquer_pour','categorie']
    list_filter = ['type_calcule','categorie']
    list_display_links = ['id']

admin.site.register(Rubrique, RubriqueAdmin)

#---| Prestation Automatique |---------------------------------------------------------------------------------------------------------------------


class PrestationAdmin(admin.ModelAdmin):
    search_fields = ['rubrique__designation',]
    list_display = ['id','rubrique','bareme','get_categorie','type_tc','dangereux','frigo','prix','groupage' ]
    list_filter = ['bareme','type_tc','dangereux','frigo','rubrique__categorie','groupage']
    list_display_links = ['id']
    
    @admin.display(description='CATEGORIE',)
    def get_categorie(self, obj):
        return obj.rubrique.categorie
    
admin.site.register(Prestation, PrestationAdmin)

#---| Prestation Automatique |---------------------------------------------------------------------------------------------------------------------


class PrestationOccasionnelleAdmin(admin.ModelAdmin):
    search_fields = ['rubrique','tc__tc',]
    list_display = ['id','rubrique','tc','get_article','prix','date' ]
    list_display_links = ['id']

    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.tc.article


      
admin.site.register(PrestationOccasionnelle, PrestationOccasionnelleAdmin)

#---| Prestation Automatique |---------------------------------------------------------------------------------------------------------------------


class PrestationOccasionnelleGroupageAdmin(admin.ModelAdmin):
    search_fields = ['rubrique','sous_article__tc__tc','sous_article__tc__article__gros__numero']
    list_display = ['id','rubrique','get_gros','get_article','get_tc','sous_article','prix','date' ]
    list_display_links = ['id']

    @admin.display( description='Gros',)
    def get_gros(self, obj):
        return obj.sous_article.tc.article.gros.numero
    
    @admin.display( description='Article',)
    def get_article(self, obj):
        return obj.sous_article.tc.article.numero

    @admin.display( description='Tc',)
    def get_tc(self, obj):
        return obj.sous_article.tc.tc


      
admin.site.register(PrestationOccasionnelleGroupage, PrestationOccasionnelleGroupageAdmin)

#---| Prestation Article |---------------------------------------------------------------------------------------------------------------------


class PrestationArtileAdmin(admin.ModelAdmin):
    search_fields = ['designation','bareme','type_tc', ]
    list_display = ['id','bareme','rubrique','prix' ]
    list_filter = ['bareme',]
    list_display_links = ['id']

admin.site.register(PrestationArticle, PrestationArtileAdmin)

#---| Sejour |---------------------------------------------------------------------------------------------------------------------

class SejourAdmin(admin.ModelAdmin):
    search_fields = ['bareme__designation']
    list_display = ['id','bareme','type_tc','dangereux','frigo','jour_min','jour_max','prix', ]
    list_filter = ['bareme','type_tc','dangereux','frigo']
    list_display_links = ['id']

admin.site.register(Sejour, SejourAdmin)


# #---| Sejour Tc Groupage |---------------------------------------------------------------------------------------------------------------------
class SejourTcGroupageAdmin(admin.ModelAdmin):
    search_fields = ['bareme','type_tc',]
    list_display = ['id','bareme','type_tc','dangereux','frigo','jour_min','jour_max','prix', ]
    list_filter = ['bareme','type_tc','dangereux','frigo']
    list_display_links = ['id']

admin.site.register(SejourTcGroupage, SejourTcGroupageAdmin)

# #---| Sejour Spus Article Groupage |---------------------------------------------------------------------------------------------------------------------
class SejourSousArticleGroupageAdmin(admin.ModelAdmin):
    search_fields = ['bareme',]
    list_display = ['id','bareme','dangereux','jour_min','jour_max','prix', ]
    list_filter = ['bareme','dangereux']
    list_display_links = ['id']

admin.site.register(SejourSousArticleGroupage, SejourSousArticleGroupageAdmin)


#---| Branchement |---------------------------------------------------------------------------------------------------------------------

class BranchementAdmin(admin.ModelAdmin):
    search_fields = ['bareme','type_tc',]
    list_display = ['id','bareme','type_tc','jour_min','jour_max','prix', ]
    list_filter = ['bareme','type_tc',]
    list_display_links = ['id']

admin.site.register(Branchement, BranchementAdmin)

#---| Prestation Groupage |---------------------------------------------------------------------------------------------------------------------

class PrestationGroupageAdmin(admin.ModelAdmin):
    search_fields = ['rubrique__designation',]
    list_display = ['id','bareme','rubrique','dangereux','prix' ]
    list_display_links = ['rubrique']
    list_filter = ['bareme','dangereux']


admin.site.register(PrestationGroupage, PrestationGroupageAdmin)

#---| Prestation Visite Groupage |---------------------------------------------------------------------------------------------------------------------

 
class PrestationVisiteGroupageAdmin(admin.ModelAdmin):
    search_fields = ['volume_min',]
    list_display = ['id','bareme','dangereux','volume_min','volume_max','prix' ]
    list_display_links = ['id']
    list_filter = ['bareme','dangereux']

admin.site.register(PrestationVisiteGroupage, PrestationVisiteGroupageAdmin)
