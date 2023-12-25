from pyexpat import model
from django.db import connections, models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.core.exceptions import ValidationError
from django.db.models.expressions import OrderBy
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms import CharField 
from app.models import *
from simple_history.models import HistoricalRecords
from src.methods import *

def getCode():
    rubrique = Rubrique.objects.all()
    last_rubrique = Rubrique.objects.all().order_by('id').last()
    if not last_rubrique :
         return 'RS001'
    code = last_rubrique.code
    code_int = int(code.split('RS')[-1])
    new_code_int = int(code_int) + 1
    new_code_no = 'RS' +format(new_code_int, '03d')  
    return new_code_no

class Bareme(models.Model): 
    designation = models.CharField(max_length=100)
    starting_date =  models.DateField(auto_now=False, auto_now_add=False, blank = True, null = True) 
    ending_date =  models.DateField(auto_now=False, auto_now_add=False, blank = True, null = True) 
    accostage = models.BooleanField(default=False,verbose_name="à partir de la date d'accostage", blank=True, null=True)
    history = HistoricalRecords()

    def get_prestations(self): 
        return self.prestation_set.all()

    def get_prestations_article(self): 
        return self.prestationarticle_set.all() 

    def get_sejour(self): 
        return self.sejour_set.all() 

    def get_branchement(self): 
        return self.branchement_set.all()    

    def get_regimes(self): 
        return self.regime_set.all()   

    class Meta:
        verbose_name_plural = "baremes"

    def clean(self):
        if self.id is None : 
            if self.starting_date > self.ending_date: 
                raise ValidationError({'ending_date': "Vous ne pouvez pas définir une plage de temps négative, Veuillez sélectionner une date de fin différente."})

    def __str__(self):
        return self.designation 

class Regime(models.Model): 
    designation = models.CharField(max_length=50, verbose_name="Regime désignation")
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.SET_NULL, null=True, blank=True)
    METHOD_CALCULE = (
        ("A la date d'accostage", "A la date d'accostage"),
        ("A l'entéée du premier TC", "A l'entéée du premier TC"),
        ("A l'entrée du dernier TC", "A l'entrée du dernier TC"),
    )
  
    methode_calcule = models.CharField(choices=METHOD_CALCULE, default=2, max_length=50)
    TYPE_CALCULE = (
        ("hard", "hard"),
        ("easy", "easy"),
    )
    enterposage = models.CharField(choices=TYPE_CALCULE, verbose_name="Regime enterposage", default=1, max_length=5)

    color = models.CharField(max_length=50,verbose_name="Regime color", null=True) 

    parc = models.ForeignKey("reference.Parc", on_delete=models.SET_NULL,verbose_name="Regime parc", null=True, blank=True)

    def get_mehtode_calcule(self): 
        return self.methode_calcule

    def __str__(self) -> str:
        return self.designation


class RubriqueManager(models.Manager): 
    def automatique(self): 
        return self.filter(categorie="Automatique")

    def occasionnelle(self):
        return self.filter(categorie="Préstation occasionnelle")


class Rubrique(models.Model): 
    code = models.CharField(max_length=50,default=getCode)
    designation = models.CharField(max_length=100)
    TYPES_CALCULE =  [
        ('Calcule par unité TC' , 'Calcule par unité TC') , 
        ('Calcule par unité JOUR' , 'Calcule par unité JOUR'),
        ('Calcule par unité TC X JOUR' , 'Calcule par unité TC X JOUR'),
        ('Calcule par unité ARTICLE' , 'Calcule par unité ARTICLE'),
        ('A la demande' , 'A la demande'),
    ]
    type_calcule = models.CharField(max_length=30, choices= TYPES_CALCULE) 
    TYPES_RUBRIQUE =  [
        ('Automatique' , 'Automatique') , 
        ('Clarck Intégral' , 'Clarck Intégral') , 
        ('Clarck Partiel' , 'Clarck Partiel') , 
        ('Dangereux' , 'Dangereux'),
        ('Dépotage' , 'Dépotage'),
        ('Manutentions humaines Intégral' , 'Manutentions humaines Intégral'),
        ('Manutentions humaines Partiel' , 'Manutentions humaines Partiel'),
        ('Préstation occasionnelle' , 'Préstation occasionnelle'),
        ('Scanner' , 'Scanner'),
        ('Visite' , 'Visite'),
        ('Groupage' , 'Groupage'),
        ('Entreposage groupage' , 'Entreposage groupage'),
    ]    
    categorie = models.CharField(max_length=30, choices= TYPES_RUBRIQUE, null=True, blank =True) 
    APPLICATION =  [
    ('Client' , 'Client') , 
    ('Groupeur' , 'Groupeur') , 
    ('Client et Groupeur' , 'Client et Groupeur') , 
    ]
    appliquer_pour = models.CharField(max_length=30, choices= APPLICATION,default='Client') 
    direction = models.ForeignKey("reference.Direction", on_delete=models.PROTECT, null=True)
    code_comptable = models.CharField(max_length=30, null=True, blank=True) 
    history = HistoricalRecords()

    objects = RubriqueManager()

    class Meta:
        verbose_name_plural = "rebriques"

    def __str__(self):
        return self.designation
    
class Prestation(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT)
    rubrique = models.ForeignKey("bareme.Rubrique",on_delete=models.CASCADE)
    type_tc = models.ForeignKey("reference.Type", on_delete=models.PROTECT)
    dangereux = models.BooleanField(default=False, null = True)
    frigo = models.BooleanField(default=False, null = True)
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    groupage = models.BooleanField(default=False, null = True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "prestations"

    def clean(self): 
        if self.id is None :             
            prestation_list = Prestation.objects.filter(rubrique = self.rubrique ,bareme=self.bareme,type_tc=self.type_tc,dangereux=self.dangereux,frigo=self.frigo, groupage=self.groupage)

            if len(prestation_list) > 0 :
                raise ValidationError("Préstation existe déja.")

    def __str__(self):
        return str(self.rubrique) + " " + str(self.type_tc)
    
class PrestationOccasionnelle(models.Model): 
    rubrique = models.CharField(max_length=50) 
    tc = models.ForeignKey("app.Tc", on_delete=models.CASCADE)
    date =  models.DateField(auto_now=False, auto_now_add=False, blank = True, null = True) 
    prix = models.DecimalField(max_digits=19, decimal_places=3)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "prestations occasionnelle"

    def __str__(self):
        return str(self.rubrique) + " " + str(self.tc)

class PrestationOccasionnelleGroupage(models.Model): 
    rubrique = models.CharField(max_length=50) 
    sous_article = models.ForeignKey("app.SousArticle", on_delete=models.CASCADE)
    date =  models.DateField(auto_now=False, auto_now_add=False, blank = True, null = True) 
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "prestations occasionnelle groupage"

    def __str__(self):
        return str(self.rubrique) + " " + str(self.tc)

class PrestationArticle(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT)
    rubrique = models.ForeignKey("bareme.Rubrique",on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    history = HistoricalRecords()
    groupage = models.BooleanField(default=False, null = True, blank=True)

    class Meta:
        verbose_name_plural = "prestations article"

    def clean(self): 
        if self.id is None :             
            prestation_list = PrestationArticle.objects.filter(rubrique = self.rubrique ,bareme=self.bareme,groupage=self.groupage)

            if len(prestation_list) > 0 :
                raise ValidationError("Préstation existe déja.")

    def __str__(self):
        return str(self.rubrique) 

class Sejour(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT)
    type_tc = models.ForeignKey("reference.Type", on_delete=models.PROTECT)
    dangereux = models.BooleanField(default=False)
    frigo = models.BooleanField(default=False)
    jour_min = models.IntegerField(blank=True,)   
    jour_max = models.IntegerField()
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    history = HistoricalRecords()

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "séjours"

    def clean(self):
        if self.id is None : 
            sejour_list = Sejour.objects.filter(bareme = self.bareme,type_tc=self.type_tc,dangereux=self.dangereux, frigo=self.frigo).order_by("-jour_max")
            if len(sejour_list) == 0 : 
                min = 1 
            else: 
                min = sejour_list.first().jour_max + 1

            if min >= self.jour_max: 
                raise ValidationError({"jour_max":"Le jour max doit être supérieur au jour min."})
            


    def clean(self, *args, **kwargs):
        sejour_list = Sejour.objects.filter(bareme = self.bareme,type_tc=self.type_tc,dangereux=self.dangereux, frigo=self.frigo).order_by("-jour_max")
        if len(sejour_list) == 0 : 
            self.jour_min = 1 
        else: 
            if(self.jour_min is None): 
                self.jour_min = sejour_list.first().jour_max + 1


    def delete(self, *args, **kwargs):
        sejour_list = Sejour.objects.filter(bareme = self.bareme,type_tc=self.type_tc,jour_min__gt= self.jour_max)
        for item in sejour_list: 
            item.delete()
            
        super(Sejour, self).delete(*args, **kwargs)

    def __str__(self):
        return "de "+str(self.jour_min)+" jours a "+str(self.jour_max) 


class SejourTcGroupage(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT)
    type_tc = models.ForeignKey("reference.Type", on_delete=models.PROTECT)
    dangereux = models.BooleanField(default=False)
    frigo = models.BooleanField(default=False)
    jour_min = models.IntegerField(blank=True,)   
    jour_max = models.IntegerField()
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    history = HistoricalRecords()

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "séjours groupage"

    def clean(self):
        if self.id is None : 
            sejour_list = SejourTcGroupage.objects.filter(bareme = self.bareme,type_tc=self.type_tc,dangereux=self.dangereux, frigo=self.frigo).order_by("-jour_max")
            if len(sejour_list) == 0 : 
                min = 1 
            else: 
                min = sejour_list.first().jour_max + 1

            if min >= self.jour_max: 
                raise ValidationError({"jour_max":"Le jour max doit être supérieur au jour min."})
            


    def clean(self, *args, **kwargs):
        sejour_list = SejourTcGroupage.objects.filter(bareme = self.bareme,type_tc=self.type_tc,dangereux=self.dangereux, frigo=self.frigo).order_by("-jour_max")
        if len(sejour_list) == 0 : 
            self.jour_min = 1 
        else: 
            if(self.jour_min is None): 
                self.jour_min = sejour_list.first().jour_max + 1


    def delete(self, *args, **kwargs):
        sejour_list = SejourTcGroupage.objects.filter(bareme = self.bareme,type_tc=self.type_tc,jour_min__gt= self.jour_max)
        for item in sejour_list: 
            item.delete()
            
        super(SejourTcGroupage, self).delete(*args, **kwargs)

    def __str__(self):
        return "de "+str(self.jour_min)+" jours a "+str(self.jour_max) 


class SejourSousArticleGroupage(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT)
    dangereux = models.BooleanField(default=False)
    jour_min = models.IntegerField(blank=True,)   
    jour_max = models.IntegerField()
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    history = HistoricalRecords()

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "séjours Sous article"

    def clean(self):
        if self.id is None : 
            sejour_list = SejourSousArticleGroupage.objects.filter(bareme = self.bareme,dangereux=self.dangereux).order_by("-jour_max")
            if len(sejour_list) == 0 : 
                min = 1 
            else: 
                min = sejour_list.first().jour_max + 1

            if min >= self.jour_max: 
                raise ValidationError({"jour_max":"Le jour max doit être supérieur au jour min."})
            


    def clean(self, *args, **kwargs):
        sejour_list = SejourSousArticleGroupage.objects.filter(bareme = self.bareme,dangereux=self.dangereux).order_by("-jour_max")
        if len(sejour_list) == 0 : 
            self.jour_min = 1 
        else: 
            if(self.jour_min is None): 
                self.jour_min = sejour_list.first().jour_max + 1


    def delete(self, *args, **kwargs):
        sejour_list = SejourSousArticleGroupage.objects.filter(bareme = self.bareme,jour_min__gt= self.jour_max)
        for item in sejour_list: 
            item.delete()
            
        super(SejourSousArticleGroupage, self).delete(*args, **kwargs)

    def __str__(self):
        return "de "+str(self.jour_min)+" jours a "+str(self.jour_max) 

class Branchement(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT)
    type_tc = models.ForeignKey("reference.Type", on_delete=models.PROTECT)
    jour_min = models.IntegerField(blank=True,)   
    jour_max = models.IntegerField()
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "branchements"   

    class Meta: 
        ordering = ["id"]
        
    def clean(self):
        if self.id is None : 
            Branchement_list = Branchement.objects.filter(bareme = self.bareme,type_tc=self.type_tc).order_by("-jour_max")
            if len(Branchement_list) == 0 : 
                min = 1 
            else: 
                min = Branchement_list.first().jour_max + 1

            if min >= self.jour_max: 
                raise ValidationError({"jour_max":"Le jour max doit être supérieur au jour min."})
            
    def save(self, *args, **kwargs):
        Branchement_list = Branchement.objects.filter(bareme = self.bareme,type_tc=self.type_tc).order_by("-jour_max")
        if len(Branchement_list) == 0 : 
            self.jour_min = 1 
        else: 
            self.jour_min = Branchement_list.first().jour_max + 1

        super(Branchement, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Branchement_list = Branchement.objects.filter(bareme = self.bareme,type_tc=self.type_tc,jour_min__gt= self.jour_max)
        for item in Branchement_list: 
            item.delete()
        super(Branchement, self).delete(*args, **kwargs)

    def __str__(self):
        return "de "+str(self.jour_min)+" jours a "+str(self.jour_max) 
    


class PrestationGroupage(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", verbose_name=("Bareme groupage"), on_delete=models.CASCADE) 
    rubrique = models.ForeignKey("bareme.Rubrique", on_delete=models.CASCADE) 
    dangereux = models.BooleanField(default=False, blank=True, null=True)
    prix = models.DecimalField(max_digits=19, decimal_places=2)
    
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "prestations groupage"

class PrestationVisiteGroupage(models.Model): 
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT)
    dangereux = models.BooleanField(default=False)
    volume_min = models.IntegerField(blank=True,)   
    volume_max = models.IntegerField()
    prix = models.DecimalField(max_digits=19, decimal_places=2)


    class Meta:
        ordering = ["id"]
        verbose_name_plural = "prestations visite groupage"

    def clean(self):
        if self.id is None : 
            sejour_list = PrestationVisiteGroupage.objects.filter(bareme = self.bareme,dangereux=self.dangereux).order_by("-volume_max")
            if len(sejour_list) == 0 : 
                min = 1 
            else: 
                min = sejour_list.first().jour_max 

            if min >= self.jour_max: 
                raise ValidationError({"volume_max":"Le volume max doit être supérieur au volume min."})
            


    def clean(self, *args, **kwargs):
        sejour_list = PrestationVisiteGroupage.objects.filter(bareme = self.bareme,dangereux=self.dangereux).order_by("-volume_max")
        if len(sejour_list) == 0 : 
            self.volume_min = 1 
        else: 
            self.volume_min = sejour_list.first().volume_max 


    def delete(self, *args, **kwargs):
        sejour_list = PrestationVisiteGroupage.objects.filter(bareme = self.bareme,volume_min__gt= self.volume_max)
        for item in sejour_list: 
            item.delete()
            
        super(PrestationVisiteGroupage, self).delete(*args, **kwargs)

    def __str__(self):
        return "de "+str(self.volume_min)+" à "+str(self.volume_max) +" M3"