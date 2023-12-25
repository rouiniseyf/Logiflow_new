from django.contrib import admin
from .models import *




#---| Article |------------------------------------------------------------------------------------------------------------------
class TcInline(admin.StackedInline):
    model = Tc
    extra = 1   


 
class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['numero','gros__numero',]
    list_display = ['id','numero','gros','bl','groupage','depote','date_depotage','client','transitaire','designation','observation_depotage' ]
    list_display_links = ['numero']
    raw_id_fields = ('client','transitaire')


    inlines = [TcInline]

admin.site.register(Article, ArticleAdmin)

#---| Scelle |------------------------------------------------------------------------------------------------------------------
 
class ScelleAdmin(admin.ModelAdmin):
    search_fields = ['numero','tc__tc',]
    list_display = ['numero','tc','date_creation','type_scelle' ]
    list_display_links = ['numero']
    list_filter = (
            'date_creation',
        )
admin.site.register(Scelle, ScelleAdmin)

#---| Sous article |-------------------------------------------------------------------------------------------------------------

class SousArticleAdmin(admin.ModelAdmin):
    search_fields = ['numero','tc__article__numero',]
    list_display = ['id','numero','tc','get_article','designation','poids','nombre_colis','client','transitaire' ]
    list_display_links = ['numero']

    
    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.tc.article
    
admin.site.register(SousArticle, SousArticleAdmin)



class TcAdmin(admin.ModelAdmin):
    readonly_fields = ['bulletins','current_scelle','receved_by','article']

    search_fields = ['tc','article__numero','article__gros__gros',]
    list_display = ['tc','article','type_tc','poids','bulletins','current_scelle','get_client','date_sortie_port','date_entree_port_sec','date_sortie_port_sec','receved_by','receved','billed']
    list_display_links = ['tc']



    @admin.display( description='CLIENT',)
    def get_client(self, obj):
        return obj.article.client
            
    actions = ['undo_exit']
    @admin.action(description='Change selected containers exited status to false')
    def undo_exit(self, request, queryset):
        updated = queryset.update(billed=False)

        
admin.site.register(Tc, TcAdmin)


#---| Gros |-----------------------------------------------------------------------------------------------------------------------

class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1   

class GrosAdmin(admin.ModelAdmin):
    readonly_fields = ['port_emission','port_reception','navire',]
    search_fields = ['numero',  ]
    list_display = ['id','numero','escale','accostage','port_emission','port_reception','navire','armateur','consignataire','regime' ]
    list_display_links = ['numero']
    inlines = [ArticleInline]
admin.site.register(Gros, GrosAdmin)




#---| Bulletains d'escorte |-------------------------------------------------------------------------------------------------------

class BulletinsEscortAdmin(admin.ModelAdmin):
    search_fields = ['numero', ]
    list_display = ['id','numero','date_creation','gros','charge_chargement','charge_reception','loaded' ]
    list_display_links = ['numero']
admin.site.register(BulletinsEscort, BulletinsEscortAdmin)

#---| visite |-------------------------------------------------------------------------------------------------------------------
class VisiteItemInline(admin.StackedInline):
    model = VisiteItem
    extra = 1 

class VisiteAdmin(admin.ModelAdmin):
    search_fields = ['numero','gros__numero']
    list_display = ['id','numero','date_creation','gros','article','badge',]
    list_display_links = ['numero']
    inlines = [VisiteItemInline]

admin.site.register(Visite, VisiteAdmin)

#---| Visite item |---------------------------------------------------------------------------------------------------------------



class VisiteItemAdmin(admin.ModelAdmin):
    search_fields = ['tc__tc','tc__article__numero','visite__numero']
    list_display = ['visite','scelle','get_type_tc','get_tc_tc']
    list_display_links = ['visite']

    @admin.display( description='Type Tc',)
    def get_type_tc(self, obj):
        return obj.tc.type_tc

    @admin.display( description='Tc',)
    def get_tc_tc(self, obj):
        return obj.tc.tc
    
    
admin.site.register(VisiteItem, VisiteItemAdmin)

#---| Position |---------------------------------------------------------------------------------------------------------------------

class PositionAdmin(admin.ModelAdmin):
    search_fields = ['tc', ]
    list_display = ['id','parc','zone','ligne','range','garbage','date_position' ]
    list_display_links = ['id']
admin.site.register(Position, PositionAdmin)


