from this import d
from django.db import connections, models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.core.exceptions import ValidationError
from django.db.models.expressions import OrderBy
from django.db.models.fields import BooleanField, DecimalField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ForeignObjectRel
from bareme.models import PrestationOccasionnelle, getCode
from simple_history.models import HistoricalRecords
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from billing.models import *
from src.methods import *
from django.db.models.signals import post_delete, post_save
import time 
from bareme.models import *

def getNextNumber(prefix,model):
    all = model.objects.filter(date_creation__year = date.today().year).order_by("numero")
    last = all.last()

    if not last or (last.date_creation.year != date.today().year):
        return prefix+'000001'
    else: 
        max = 0
        for record in all: 
            if int(record.numero.split(prefix)[-1]) > max : 
                max = int(record.numero.split(prefix)[-1]) 

        new_int = max + 1
        new_no = prefix + format(new_int, '06d')

    return new_no 

def getNumeroBulletins():
    return getNextNumber('BE',BulletinsEscort)

def getNumeroVisite():
    return getNextNumber('V',Visite)

class GrosManager(models.Manager): 
    def has_receved_articles(self): 
        return [item for item in self.all() if item.has_articles_with_receved_containers ]

from django.db.models import Count



class Gros(models.Model):
    numero = models.CharField(max_length=50)
    gros = models.CharField(max_length=100, blank=True, null=True)
    escale = models.CharField(max_length=100, null=True, blank=True)
    accostage = models.DateField(auto_now=False, auto_now_add=False)
    port_emission = models.ForeignKey("reference.Port", related_name="port_emission", on_delete=models.SET_NULL, null=True, blank=True)
    port_reception = models.ForeignKey("reference.Port", related_name="port_reception", on_delete=models.SET_NULL, null=True, blank=True)
    navire = models.ForeignKey("reference.Navire", on_delete=models.SET_NULL, null=True)
    armateur = models.ForeignKey("reference.Armateur", on_delete=models.SET_NULL, null=True)
    consignataire = models.ForeignKey("reference.Consignataire", on_delete=models.SET_NULL, null=True)
    bareme = models.ForeignKey("bareme.Bareme", on_delete=models.SET_NULL, null=True, blank=True)
    regime = models.ForeignKey("bareme.Regime", on_delete=models.PROTECT,null=True,verbose_name="Régime")

    @property 
    def has_articles_with_receved_containers(self):   
        return len([article for article in self.article_set.all() if article.has_receved_containers]) > 0 

    @property 
    def has_articles_with_not_receved_containers(self):  
        return len([article for article in self.article_set.all() if article.has_not_receved_containers]) > 0 

    @property 
    def has_articles_with_not_charged_containers(self):  
        return len([article for article in self.article_set.all() if article.has_not_charged_containers]) > 0 

    @property
    def gros_name(self): 
        return self.gros +" "+str(self.accostage.year)+" "+str(self.regime)
    
    @property
    def name(self): 
        return self.gros +" "+str(self.regime)


    @property 
    def containers_count(self):
        #cc = self.article_set.values_list("tc__id").aggregate(total=Count( "tc__id" ))['total']
        #Tc.objects.filter(article__gros=self).count()
        #print("xxxxxxxxxxxx",articles)
        return self.article_set.values_list("tc__id").aggregate(total=Count( "tc__id" ))['total']

    def get_bareme(self): 
        if self.bareme is None: 
            return self.regime.bareme 
        else: 
            return self.bareme 

    def container_count(self): 
        return Tc.objects.filter(article__gros__id = self.id).count()

    @property 
    def has_containers(self): 
        return self.container_count() > 0 

    @property 
    def has_groupage(self): 
        return len([article for article in self.article_set.all() if article.groupage]) > 0
    
    def get_articles_with_receved_cotainers(self): 
        return Article.objects.filter(pk__in = [article.id for article in self.article_set.all() if article.has_receved_containers])

    def get_receved_containenrs(self): 
        return ListToQuerySet([article.get_receved_containers() for article in self.article_set.all() if article.has_receved_containers],Tc)


    def get_not_receved_containenrs(self): 
        return ListToQuerySet([article.get_not_receved_containers() for article in self.article_set.all()],Tc)

    def get_not_charged_containenrs(self): 
        return ListToQuerySet([article.get_not_charged_containers() for article in self.article_set.all()],Tc)

    def get_articles(self): 
        return self.article_set.all()

    objects = GrosManager()

    class Meta:
        unique_together = [['numero', 'accostage','regime']]
        ordering = ["-id"]
        verbose_name_plural = "gros"
  
    def __str__(self):
        return self.gros +" "+ str(self.regime)

    def __unicode__(self):
        return self.gros

    def save(self, *args, **kwargs):
        self.gros = self.numero + " / " + str(self.accostage.year)
        super(Gros, self).save(*args, **kwargs)


class Article(models.Model):
    gros = models.ForeignKey("app.Gros",related_name="articles", on_delete=models.CASCADE)
    numero = models.IntegerField()
    groupage = models.BooleanField(default=False)
    date_depotage = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    depote = models.BooleanField(default=False, blank=True, null=True)
    observation_depotage = models.CharField(max_length=400, blank=True, null=True,default="R.A.S")
    bl = models.CharField(max_length=50)
    designation = models.CharField(max_length=200, blank=True, null=True)
    client = models.ForeignKey( "reference.Client", on_delete=models.SET_NULL, null=True)
    transitaire = models.ForeignKey( "reference.Transitaire", on_delete=models.PROTECT, blank=True, null=True)
    history = HistoricalRecords()

    def get_sous_articles(self): 
        return SousArticle.objects.filter(tc__article = self)
    
    def get_receved_containers(self): 
        return self.tc_set.receved()

    def date_entree_first_container(self): 
        return self.tc_set.first().date_entree_port_sec 

    def get_not_receved_containers(self): 
        return self.tc_set.not_receved()

    def get_not_charged_containers(self): 
        return self.tc_set.not_charged()

    def container_count(self): 
        return self.tc_set.all().count()

    def get_billed_containers(self): 
        return self.tc_set.billed()

    def get_not_billed_containers(self): 
        return self.tc_set.not_billed()


    def get_all_containers(self): 
        return self.tc_set.all()

    def get_all_visits(self): 
        return self.visite_set.all() 

    def get_all_proformas(self): 
        return self.proforma_set.all()

    def get_factures(self): 
        return Facture.objects.filter(proforma__article = self)

    def get_commands(self):
        return Commande.objects.filter(bon_commande__in = self.boncommande_set.all())

    def get_factures_complementaire(self): 
        return FactureComplementaire.objects.filter(facture__in = self.get_factures())

    def get_factures_avoire(self): 
        FactureAvoire.objects.filter(facture__in = self.get_factures())
        return FactureAvoire.objects.filter(facture__in = self.get_factures())

    def get_prestations_occasionnelle(self): 
        return PrestationOccasionnelle.objects.filter(tc__in = self.get_all_containers())

    def get_fist_entered_container(self): 
        return self.tc_set.all().order_by("date_entree_port_sec").first()

    def get_last_entered_container(self): 
        return self.tc_set.all().order_by("-date_entree_port_sec").first()
        
    @property 
    def has_receved_containers(self):   
        return self.tc_set.filter(receved = True).exists() 

    @property 
    def has_not_charged_containers(self):   
        return self.tc_set.not_charged().exists() 

    @property 
    def has_not_receved_containers(self):   
        return self.tc_set.filter(receved = False).exists() 
    @property
    def invoiced(self): 
        if self.get_billed_containers().count() == self.get_all_containers().count(): 
            return True 
        else: 
            return False 

    class Meta:
            ordering = ["gros__accostage"]
            verbose_name_plural = "articles"

    def __str__(self):
        return str(self.numero) + " | " + str(self.gros)


class Position(models.Model):
    parc = models.ForeignKey("reference.parc", on_delete=models.PROTECT)
    zone = models.ForeignKey("reference.Zone", on_delete=models.PROTECT)
    tc = models.ForeignKey("app.Tc", on_delete=models.PROTECT)
    ligne = models.IntegerField()
    range = models.IntegerField()
    garbage = models.IntegerField()
    date_position = models.DateField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["date_position"]
        verbose_name_plural = "positions"

    def __str__(self):
        return str(self.parc) + " | Z" + str(self.zone) + " L" + str(self.ligne) + " R" + str(self.range) + " G" + str(self.garbage)

    def clean(self):
        last = Position.objects.filter(tc=self.tc).order_by("-id").first()
        if last != None:
            if(self.ligne == last.ligne and self.range == last.range and self.zone == last.zone):
                raise ValidationError("Aucune modification apportée")
        if self.ligne > self.zone.lignes:
            raise ValidationError(
                {"ligne": "Cette ligne n'existe pas. veuillez choisir une valeur inférieure à "+str(self.zone.lignes + 1)})

        if self.ligne > self.zone.lignes:
            raise ValidationError(
                {"ligne": "Cette ligne n'existe pas. veuillez choisir une valeur inférieure à "+str(self.zone.lignes + 1)})

        if self.range > self.zone.ranges:
            raise ValidationError(
                {"range": "Cette rangé n'existe pas. veuillez choisir une valeur inférieure à "+str(self.zone.lignes + 1)})

        if self.garbage > self.zone.gerbage:
            raise ValidationError(
                {"garbage": "La hauteur maximale dans cette zone doit être inférieure à "+str(self.zone.garbage + 1)})


class BulletinsManager(models.Manager): 
    def not_loaded(self): 
        return self.filter(loaded = False)

    def loaded(self): 
        return self.filter(loaded = True)

    def receved(self): 
        return self.filter(receved = True)

    def not_receved(self): 
        return self.filter(receved = False)

class BulletinsEscort(models.Model):
    bulletins = models.CharField(max_length=50, blank=True, null=True, unique=True)
    numero = models.CharField(max_length=9, default=getNumeroBulletins)
    date_creation = models.DateField(auto_now=False, auto_now_add=False)
    gros = models.ForeignKey("app.Gros", on_delete=models.PROTECT)
    charge_chargement = models.ForeignKey(User, related_name="agent_charge_chargement", on_delete=models.PROTECT, null=True, blank=True)
    charge_reception = models.ForeignKey(User, related_name="agent_charge_creation", on_delete=models.PROTECT, null=True, blank=True)
    loaded = models.BooleanField(default=False)
    receved = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        ordering = ["numero"]
        verbose_name_plural = "bulletins d'escort"

    objects = BulletinsManager()

    @property 
    def has_lines(self): 
        containers = self.tc_set.all()
        return len(containers)  > 0 

    def __str__(self):
        return self.bulletins

    def clean(self):
        if self.id is None : 
            if self.gros.has_articles_with_not_charged_containers == False: 
                raise ValidationError("le gros sélectionné n'a pas d'articles avec des contenants non reçus.")
        super(BulletinsEscort, self).clean()

    def save(self):
        if self.id is None : 
            self.bulletins = self.numero + " / " + str(self.date_creation.year)

        super(BulletinsEscort, self).save()



class TcManager(models.Manager): 
    def receved(self): 
        return self.filter(receved = True)

    def not_receved(self): 
        return self.filter(receved = False)

    def billed(self): 
        return self.filter(billed = True)

    def not_billed(self): 
        return self.filter(billed = False)

    def not_charged(self): 
        return self.filter(bulletins = None)

    def charged(self): 
        return self.filter(bulletins__isnull = False)


class Tc(models.Model):
  
    article = models.ForeignKey("app.Article", on_delete=models.CASCADE)
    type_tc = models.ForeignKey("reference.Type", on_delete=models.PROTECT, blank=True, null=True)
    dangereux = models.BooleanField(default=False, blank=True, null=True)
    frigo = models.BooleanField(default=False, blank=True, null=True)
    tc = models.CharField(max_length=50)
    tar = models.IntegerField()
    poids = models.CharField(max_length=50) 

    bulletins = models.ForeignKey("app.BulletinsEscort", on_delete=models.SET_NULL, blank=True, null=True)
    matricule_camion = models.CharField(max_length=50, blank=True, null=True)
    date_sortie_port = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    date_entree_port_sec = models.DateTimeField( auto_now=False, auto_now_add=False, blank=True, null=True)
    date_sortie_port_sec = models.DateTimeField( auto_now=False, auto_now_add=False, blank=True, null=True)
    receved_by = models.ForeignKey( User, related_name="agent_charge_reception", on_delete=models.PROTECT, null=True, blank=True)
    billed = models.BooleanField(default=False, blank=True, null=True)
    etat = models.CharField(max_length=50, blank=True, null=True)
    observation_chargement = models.CharField( max_length=200, blank=True, null=True, default="-")
    observation_reception = models.CharField( max_length=200, blank=True, null=True, default="-")
    observation_entree_port_sec = models.CharField( max_length=200, blank=True, null=True, default="-")
    observation_sortie_port_sec = models.CharField( max_length=200, blank=True, null=True, default="-")
    current_scelle = models.ForeignKey("app.scelle", verbose_name=("Scelle"),related_name="Scelle" ,on_delete=models.SET_NULL, null=True, blank = True)
    receved = models.BooleanField(default=False)
    
    objects = TcManager()

    def set_as_billed(self): 
        self.billed = True 
        self.save()

    def set_as_not_billed(self): 
        self.billed = False
        self.save()

    def get_current_position(self): 
        return self.position_set.all().order_by('id').last()

    def get_prestations_occasionnelle(self): 
        return self.prestationoccasionnelle_set.all()

    def vu_a_quai(self): 
        return (self.date_entree_port_sec is not None)

    class Meta:
        ordering = ["article__gros__accostage"]
        verbose_name_plural = "tcs"

    def __str__(self):
        return self.tc


class SousArticle(models.Model):
    numero = models.IntegerField()
    tc = models.ForeignKey("app.Tc", on_delete=models.CASCADE)
    bl = models.CharField(max_length=50,null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    dangereux = models.BooleanField(default=False)
    nombre_colis = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    surface = models.FloatField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)
    poids = models.FloatField(blank=True, null=True)
    unite_de_visite = models.CharField(max_length=30, blank=True, null=True)
    unite_de_chargement = models.CharField(max_length=30, blank=True, null=True)
    unite_de_magasinage = models.CharField(max_length=30, blank=True, null=True)
    client = models.ForeignKey("reference.Client", on_delete=models.SET_NULL, null=True)
    transitaire = models.ForeignKey("reference.Transitaire", on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=500, blank=True, null=True)
    invoiced = models.BooleanField(default=False)
    box = models.ForeignKey("reference.Box", on_delete=models.SET_NULL, null=True)
    
    def invoiced(self): 
        return FactureGroupage.objects.filter(proforma__sous_article = self).count() > 0
    
    def get_factures(self): 
        return FactureGroupage.objects.filter(proforma__sous_article = self)
 
    def get_proformas(self): 
        return ProformaGroupage.objects.filter(sous_article = self)   
    
    def get_visites(self): 
        return VisiteGroupage.objects.filter(sous_article__id = self.id )

    def get_prestations_occasionnelle(self): 
        return self.prestationoccasionnellegroupage_set.all()

    class Meta:
        ordering = ["numero"]
        verbose_name_plural = "sous articles"

    def __str__(self):
        return str(self.numero)


class Visite(models.Model):
    TYPES_VISITE = [
        ('Visite douane', 'Visite douane'),
        ('Visite D41', 'Visite D41'),
    ]
    visite = models.CharField(max_length=50, blank=True, null=True, unique=True)
    numero = models.CharField(max_length=9, default=getNumeroVisite)
    date_creation = models.DateField(auto_now_add=True)
    date_visite = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now)
    gros = models.ForeignKey("app.Gros", on_delete=models.PROTECT)
    article = models.ForeignKey("app.Article", on_delete=models.CASCADE, blank=True, null=True)
    type_visite = models.CharField(max_length=15, choices=TYPES_VISITE)
    transitaire = models.ForeignKey("reference.Transitaire", on_delete=models.PROTECT)
    badge = models.CharField(max_length=50)
    history = HistoricalRecords()

    class Meta:
        ordering = ["numero"]
        verbose_name_plural = "visites"

    def get_items(self): 
        return self.visiteitem_set.all()

    def clean(self):
            records_count = Visite.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Visite aleady exist."})

    def __str__(self):
        return self.numero

    def save(self, *args, **kwargs):
        self.visite = self.numero + " / " + str(self.date_visite.year)
        Article.objects.filter(id=self.article.id).update(
            transitaire=self.transitaire)
        super(Visite, self).save(*args, **kwargs)


class VisiteItem(models.Model):
    visite = models.ForeignKey("app.Visite", on_delete=models.CASCADE)
    tc = models.ForeignKey("app.Tc", on_delete=models.CASCADE)
    scelle = models.CharField(max_length=50)
    observation = models.CharField(max_length=100, default="-")

    class Meta:
        verbose_name_plural = "elements visite"

    def __str__(self):
        return str(self.visite) + " " + str(self.tc)


class Scelle(models.Model):

    TYPES_SCELLE = [
        ('scelle_port', 'Scelle Port'),
        ('scelle_visite', 'Scelle Visite'),
        ('scelle_supplementaire', 'Scelle Supplémentaire'),
    ]

    tc = models.ForeignKey("app.Tc", verbose_name=("Tc"), on_delete=models.CASCADE, null=True)
    numero = models.CharField(max_length=20, unique=True)
    type_scelle = models.CharField(max_length=40,choices=TYPES_SCELLE, null= True, blank = True)
    date_creation = models.DateField(auto_now_add=True, null=True)

    history = HistoricalRecords()
    class Meta:
        ordering = ["date_creation"]
        verbose_name_plural = "scelles"

    def __str__(self):
        return  self.numero

                                     