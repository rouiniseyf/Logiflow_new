from django.contrib import admin

from .models import *




 
class VisiteGroupageAdmin(admin.ModelAdmin):
    search_fields = ['jour_min',]
    list_display = ['id','gros','article','sous_article','numero','date_creation','date_visite','type_visite','transitaire','badge',]
    list_display_links = ['numero']



admin.site.register(VisiteGroupage, VisiteGroupageAdmin)



 
class PositionGroupageAdmin(admin.ModelAdmin):
    search_fields = ['sous_article',]
    list_display = ['id','sous_article','date','box','get_article','get_gros']
    list_display_links = ['sous_article']

    @admin.display( description='ARTICLE',)
    def get_article(self, obj):
        return obj.sous_article.tc.article

    @admin.display( description='GROS',)
    def get_gros(self, obj):
        return obj.sous_article.tc.article.gros
    
admin.site.register(PositionGroupage, PositionGroupageAdmin)
