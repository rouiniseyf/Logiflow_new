class TransitaireResources(resources.ModelResource): 
    class Meta: 
        model = Cient 


class TransitaireAdmin(ImportExportModelAdmin):
    resource_class = TransitaireResources

admin.site.register(Transitaire, TransitaireAdmin)