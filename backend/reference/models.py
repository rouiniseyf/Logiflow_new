from typing import ClassVar
from django.db import connections, models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.core.exceptions import ValidationError
from django.db.models.expressions import OrderBy
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ForeignObjectRel
from src.methods import *

class Pays(models.Model): 
    code = models.IntegerField(default=0)
    alpha2 = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    nom_fr_fr = models.CharField(max_length=50, unique=True)
    nom_en_gb = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "pays"

    def __str__(self):
        return self.nom_fr_fr

class Port(models.Model): 
    raison_sociale = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=200,blank=True, null=True) 
    pays = models.ForeignKey("reference.Pays",on_delete=models.SET_NULL,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "ports"

    def __str__(self):
        return self.raison_sociale

class Type(models.Model): 
    designation = models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name_plural = "types"

    def __str__(self):
        return self.designation 

class Transitaire(models.Model): 
    raison_sociale = models.CharField(max_length=200, unique=True)
    adress = models.CharField(max_length=300,blank=True, null=True)
    email = models.EmailField(max_length=254,blank=True, null=True)
    tel = models.CharField(max_length=20,blank=True, null=True)
    soumis_tva = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "transitaires"

    class Meta:
        ordering = ['raison_sociale']
        
    def __str__(self):
        return self.raison_sociale

class Groupeur(models.Model): 
    raison_sociale = models.CharField(max_length=200, unique=True)
    adress = models.CharField(max_length=300,blank=True, null=True)
    email = models.EmailField(max_length=254,blank=True, null=True)
    tel = models.CharField(max_length=20,blank=True, null=True)
    soumis_tva = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "groupeurs"

    def __str__(self):
        return self.raison_sociale0      
    

class Navire(models.Model): 
    nom = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        verbose_name_plural = "navires"

    def __str__(self):
        return self.nom

class Armateur(models.Model): 
    raison_sociale = models.CharField(max_length=200,unique=True)
    code  = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = "armateurs"

    def __str__(self):
        return self.raison_sociale

class Consignataire(models.Model): 
    raison_sociale = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=200,blank=True, null=True)

    class Meta:
        verbose_name_plural = "consignataires"

    def __str__(self):
        return self.raison_sociale 

class Agent(models.Model): 
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "agents"

    def __str__(self):
        return self.nom +" "+self.prenom

class Client(models.Model): 
    raison_sociale = models.CharField(max_length=500,unique=True)
    adress = models.CharField(max_length=500,blank=True, null=True)
    email = models.EmailField(max_length=254,blank=True, null=True)
    tel = models.CharField(max_length=20,blank=True, null=True)
    code = models.CharField(max_length=50,blank=True, null=True)
    RC = models.CharField(max_length=50,blank=True, null=True)
    NIF = models.CharField(max_length=50,blank=True, null=True)
    AI = models.CharField(max_length=50,blank=True, null=True)
    NIS = models.CharField(max_length=50,blank=True, null=True)
    soumis_tva = models.BooleanField(default=True)
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.PROTECT, null = True, blank=True)

    class Meta:
        ordering = ['raison_sociale']
        verbose_name_plural = "clients"

    def __str__(self):
        return self.raison_sociale 

class Parc(models.Model): 
    designation  = models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name_plural = "parcs"

    def __str__(self):
        return self.designation

class Box(models.Model):
    designation  = models.CharField(max_length=50,unique=True)
    parc = models.ForeignKey("reference.Parc", on_delete=models.PROTECT, null = True)

    class Meta:
        verbose_name_plural = "boxs"

    def __str__(self):
        return self.designation
       
class Zone(models.Model): 
    parc = models.ForeignKey("reference.Parc", on_delete=models.PROTECT)
    zone = models.CharField(max_length=200, null=True, blank = True)
    lignes = models.IntegerField(null=True, blank = True)
    ranges = models.IntegerField(null=True, blank = True)
    gerbage = models.IntegerField(default=5, null=True, blank = True)

    class Meta:
        verbose_name_plural = "zones"

    def __str__(self):
        return self.zone
    
class Banque(models.Model): 
    raison_sociale = models.CharField(max_length=200,unique=True)
    adress = models.CharField(max_length=300,blank=True, null=True)
    email = models.EmailField(max_length=254,blank=True, null=True)
    tel = models.CharField(max_length=20,blank=True, null=True) 

    class Meta:
        verbose_name_plural = "banques"

    def __str__(self):
        return self.raison_sociale
    
class Direction(models.Model): 
    nom = models.CharField(max_length=200,unique=True)
    code  = models.CharField(max_length=100,blank=True, null=True)
    couleur = models.CharField(max_length=8, blank=True, null=True)
    class Meta:
        verbose_name_plural = "directions"

    def __str__(self):
        return self.nom