from logging import raiseExceptions
from multiprocessing.spawn import prepare
from xmlrpc.client import boolean
from django.contrib.admin.sites import DefaultAdminSite
from django.db import connections, models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE
from django.db.models.expressions import OrderBy
from django.db.models.fields import DecimalField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.forms import BooleanField 
from simple_history.models import HistoricalRecords
import re
from reference.models import Client 
from django.db.models import Max, Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from src.methods import *
from bareme.models import *
import app.models 
from decimal import Decimal
from groupage.models import *

def total_paiements(first_date, last_date): 


    paiamants = Paiement.objects.filter(date__range=[first_date,last_date]).aggregate(Sum('montant'))['montant__sum']

    paiamants_complementaire = PaiementFactureComplementaire.objects.filter(date__range=[first_date,last_date]).aggregate(Sum('montant'))['montant__sum']

    paiements_libre = PaiementFactureLibre.objects.filter(date__range=[first_date,last_date]).aggregate(Sum('montant'))['montant__sum']
    
    paiements_groupage = PaiementGroupage.objects.filter(date__range=[first_date,last_date]).aggregate(Sum('montant'))['montant__sum']

    if paiamants is None: 
        paiamants = 0 

    if paiamants_complementaire is None: 
        paiamants_complementaire = 0 

    if paiements_libre is None: 
        paiements_libre = 0

    if paiements_groupage is None: 
        paiements_groupage = 0
        
    return round(paiamants + paiamants_complementaire + paiements_libre+paiements_groupage,0)
    

        
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


def getNumeroProforma():
    all = Proforma.objects.filter(date_creation__year = date.today().year).order_by("id")
    last = all.last()

    if not last or (last.date_creation.year != date.today().year):
        return 'ALG000001'
    else: 
        max = 0
        for record in all: 
            if int(record.numero.split('ALG')[-1].split('FP')[-1]) > max : 
                max = int(record.numero.split('ALG')[-1].split('FP')[-1]) 

        new_int = max + 1
        new_no = 'ALG' + format(new_int, '06d')

    return new_no 

def getNumeroFacture():
    return getNextNumber('ALG',Facture)

def getNumeroBonCommande():
    return getNextNumber('BC',BonCommande)

def getNumeroBonSortie():
    return getNextNumber('BS',BonSortie)


def getNumeroBonSortieGroupage():
    return getNextNumber('BS/G/',BonSortieGroupage)

def getNumeroFactureLibre(): 
    return getNextNumber('ALG/LIBRE',FactureLibre)

def getNumeroFactureGroupage():
    return getNextNumber('GRP',FactureGroupage)

def getNumeroProformaGroupage():
    return getNextNumber('P/GRP',ProformaGroupage)


class Proforma(models.Model):
    numero = models.CharField(max_length=9,default=getNumeroProforma)
    date_creation = models.DateField(auto_now_add=True)
    gros = models.ForeignKey("app.Gros", on_delete=models.CASCADE)
    article = models.ForeignKey("app.Article", on_delete=models.CASCADE)
    date_proforma = models.DateField(auto_now=False, auto_now_add=False)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    tva = models.BooleanField(default=True, verbose_name="TVA") 
    debeur = models.BooleanField(default=False, verbose_name="DEBEUR")
    DEBEUR = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    remise = models.BooleanField(default=False)
    REMISE = models.DecimalField(max_digits=15, decimal_places=2,default=0,blank=True, null=True)
    TR = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
    valide = models.BooleanField(default=False, blank=True, null=True)
    trashed = models.BooleanField(default=False, blank=True, null=True)
    entreposage = models.BooleanField(default=True, blank=True, null=True)
    
    history = HistoricalRecords()  

    def validate(self):
        self.valide = True 
        self.save()
        self.set_containers_as_billed()

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "proformas"

    def set_containers_as_billed(self): 
        for line in self.get_groupes_lines(): 
            line.tc.set_as_billed()

    def is_container_loaded(self,tc): 
        self.get_groupes_lines().filter(tc=tc).exists()

    # get all the containers that are not billed & not loaded to any proforma yet
    def get_not_loaded_containers(self): 
        return app.models.Tc.objects.filter(pk__in = [tc.id for tc in self.article.get_receved_containers().filter(billed = False) if not self.is_container_loaded(tc)])
 
    @property 
    def total_number_of_containers(self): 
        return self.groupe_set.all().aggregate(Sum('tcs'))['tcs__sum'] 

    def get_groups(self): 
        return self.groupe_set.all()

    def get_groupes_lines(self):     
        return GroupeLigne.objects.filter(groupe__in = self.get_groups())

    def get_prestations(self): 
        return self.ligneprestation_set.all()

    def get_prestations_article(self): 
        return self.ligneprestationarticle_set.all()

    def get_enterposage(self):
        return self.groupe_set.all().aggregate(Sum('enterposage'))['enterposage__sum']

    def get_ttc_in_letters(self): 
        return decimalToText(self.TTC)

    def __str__(self):
        return self.numero + " / " + str(self.date_creation.year)  

    def clean(self):
        if self.id is None :
            records_count = Proforma.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Proforma aleady exist."})

    def calculate_totals(self): 
        total_hors_taxes = 0   
        total_hors_taxes = get_sum_hors_taxes(self.get_prestations())
        total_hors_taxes += get_sum_hors_taxes(self.get_prestations_article())    
        remise = 0     
        if self.remise: 
            total_hors_taxes,remise = calculate_remise(total_hors_taxes, self.REMISE)
        

        if self.tva: 
            total_tva = calculate_tva(total_hors_taxes) 
        else: 
            total_tva =  0  

        self.HT  = total_hors_taxes
        self.TVA  = total_tva 
        self.TR = remise
        self.TTC = total_hors_taxes + total_tva
        if self.debeur: 
            self.TTC += self.DEBEUR
        self.save()

class Groupe(models.Model): 
    proforma = models.ForeignKey("billing.Proforma",on_delete=models.CASCADE)
    type = models.ForeignKey("reference.Type", verbose_name="Container type", on_delete=models.SET_NULL,null=True)
    dangereux = models.BooleanField()
    frigo = models.BooleanField()
    tcs = models.IntegerField(null=True, blank=True)
    enterposage = models.IntegerField(null=True, blank=True)

    @property 
    def lines(self): 
        return self.groupeligne_set.all()


    class Meta:
        verbose_name_plural = "groupes"

    def __str__(self):
        return str(self.proforma) +" | "+ str(self.type) +" | " + str(self.dangereux) +" | " + str(self.frigo) 
    
class GroupeLigne(models.Model): 
    groupe = models.ForeignKey("billing.Groupe", on_delete=models.CASCADE)
    tc = models.ForeignKey("app.Tc",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "lignes groupe"

    def __str__(self):
        return self.groupe.type.designation+" "+self.tc.tc
    
class LignePrestation(models.Model): 
    proforma = models.ForeignKey("billing.Proforma",on_delete=models.CASCADE) 
    groupe = models.ForeignKey("billing.Groupe", on_delete=models.CASCADE, null=True, blank=True)
    rubrique = models.CharField(max_length=100)
    rubrique_object = models.ForeignKey("bareme.Rubrique", related_name="rubrique_prestation", on_delete=models.PROTECT, null=True, blank=True)
    tcs = models.IntegerField()
    quantite = models.IntegerField(blank=True , null= True)
    tarif = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    code_comptable = models.CharField(max_length=30, null=True, blank=True) 
   
    def update_tva_zero(self): 
        self.TVA = 0 
        self.TTC = self.HT 
        self.save()
        
    class Meta:
        verbose_name_plural = "lignes prestation"

    def save(self, *args, **kwargs):
        if self.proforma.tva: 
            self.HT = self.tarif * self.quantite
            self.TVA = (self.HT * 19) / 100
            self.TTC = self.HT + self.TVA
        else: 
            self.HT = self.tarif * self.quantite
            self.TVA = 0
            self.TTC = self.tarif * self.quantite       
                
        super(LignePrestation, self).save(*args, **kwargs)   

    def __str__(self):
        return self.rubrique 

class LignePrestationArticle(models.Model): 
    proforma = models.ForeignKey("billing.Proforma",on_delete=models.CASCADE) 
    rubrique = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    rubrique_object = models.ForeignKey("bareme.Rubrique", related_name="rubrique_prestation_article", on_delete=models.PROTECT, null=True, blank=True)
    code_comptable = models.CharField(max_length=30, null=True, blank=True) 

    class Meta:
        verbose_name_plural = "lignes prestation article"

    def update_tva_zero(self): 
        self.TVA = 0 
        self.TTC = self.HT 
        self.save()
        
    def save(self, *args, **kwargs):
        if self.proforma.tva: 
            self.HT = self.tarif 
            self.TVA = (self.HT * 19) / 100
            self.TTC = self.HT + self.TVA
        else: 
            self.HT = self.tarif 
            self.TVA = 0
            self.TTC = self.tarif       
                
        super(LignePrestationArticle, self).save(*args, **kwargs)   

    def __str__(self):
        return self.rubrique 

class BonCommande(models.Model): 
    numero = models.CharField(max_length=50, default=getNumeroBonCommande)
    date_creation = models.DateField(auto_now_add=True) 
    article = models.ForeignKey("app.Article",on_delete=models.CASCADE)

    def get_commands(self): 
        return self.commande_set.all()
 

    class Meta:
        ordering = ["-numero"]
        verbose_name_plural = "bons de commande"

    def clean(self):
            records_count = BonCommande.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Bon Commande aleady exist."})

    def __str__(self):
        return self.numero + str(self.date_creation.year)
    
class Commande(models.Model): 
    bon_commande = models.ForeignKey(BonCommande, verbose_name=("Bon de Commande"), on_delete=models.CASCADE)
    tc = models.ForeignKey("app.Tc", verbose_name= "Contenaire", on_delete=models.CASCADE)
    TYPE =  [
        ('Clarck Intégral' , 'Clarck Intégral') , 
        ('Clarck Partiel' , 'Clarck Partiel') , 
        ('Manutentions humaines Intégral' , 'Manutentions humaines Intégral') , 
        ('Manutentions humaines Partiel' , 'Manutentions humaines Partiel') , 
        ]
    type = models.CharField(choices=TYPE,max_length=50)   
    quantite = models.IntegerField()
    observation = models.CharField(max_length=100, default="-")
    rubrique_object = models.ForeignKey("bareme.Rubrique", related_name="rubrique_commande", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = "commandes"

    def __str__(self):
        return self.tc.tc + " " + self.type + " " + str(self.quantite)
    

class Facture(models.Model): 
    numero = models.CharField(max_length=9,default=getNumeroFacture)
    date_creation = models.DateField(auto_now_add=True)
    proforma = models.ForeignKey("billing.Proforma", on_delete=models.CASCADE)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TR = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    DEBEUR = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    timber = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0)
    paid = models.BooleanField(default=False, null= False, blank= False)
    a_terme  = models.BooleanField(default=False, null= False, blank= False)
    history = HistoricalRecords()   

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "factures"

    def validate_proforma(self): 
        self.HT = self.proforma.HT
        self.TVA = self.proforma.TVA
        self.TR = self.proforma.TR
        self.DEBEUR = self.proforma.DEBEUR 
        self.TTC = self.proforma.TTC
        self.proforma.validate()

    def get_total_paiments(self): 
        if self.paiement_set.all().count() > 0 : 
            return self.paiement_set.all().aggregate(total=Sum('montant'))['total']
        else: 
            return 0   

    def get_paiements(self): 
        return self.paiements_set.all()

    def get_total_cheque_paiaments(self): 
        total = self.paiement_set.filter(mode="Chèque").aggregate(total=Sum('montant'))['total']
        if total is None: 
            return 0 
        else: 
            return total 

    def get_factures_commplimentaire(self): 
        return self.facturecomplementaire_set.all() 
    
    def get_factures_avoire(self):
        return self.factureavoire_set.all()

    def get_paiements(self): 
        return self.paiement_set.all()

    def pay_a_terme(self) : 
        self.a_terme = True
        self.save()


    def refrech_status(self):
        if self.get_total_paiments() >= self.TTC: 
            self.paid = True 
        else: 
            self.paid = False 
        self.save()
    
    def add_paiament_espece(self,montant):
        timber = montant - (self.TTC - self.get_total_cheque_paiaments())
        self.timber = timber 
        ttc = self.TTC + timber 
        self.TTC = ttc

    @property
    def unpaid_espece(self): 
        total, timber = calculate_timber(self.unpaid)
        return total

    @property 
    def unpaid(self): 
        try:
            return self.TTC - self.total_paid 
        except: 
            pass
        
    @property 
    def total_paid(self): 
        total = self.get_total_paiments()
        if total is None: 
            total = 0
        return total


    @property
    def has_facture_complementaire(self): 
        return self.facturecomplementaire_set.all().exists()

    @property
    def has_facture_avoire(self): 
        return self.factureavoire_set.all().exists()

    @property 
    def facture_number(self): 
        return str(self.numero)+"/"+str(self.proforma.date_proforma.year) 
    
    @property
    def client(self): 
        return self.proforma.article.client.raison_sociale+" G-"+str(self.proforma.gros.numero)+" A-"+str(self.proforma.article.numero)
    
    def get_factrue_lines(self): 
        prestations = self.proforma.ligneprestation_set.values('proforma','rubrique','rubrique_object','rubrique_object__direction__code','tarif','HT','TVA','TTC',"code_comptable")
        prestations_article = self.proforma.ligneprestationarticle_set.values('proforma','rubrique','rubrique_object','rubrique_object__direction__code','tarif','HT','TVA','TTC',"code_comptable")
        return prestations.union(prestations_article)
       
    def get_billing_info(self):
        context = {
            "facture" : self,
            "ht_before_remise": self.HT + self.TR,
            "date_entree":  self.proforma.article.date_entree_first_container(),
            "proforma" : self.proforma,
            "groups" : self.proforma.get_groups(),
            "groups_lignes" : self.proforma.get_groupes_lines(),
            "lignes_prestations" : self.proforma.get_prestations(),
            "lignes_prestations_article" : self.proforma.get_prestations_article(),
            "tcs" : self.proforma.article.container_count(),
            "enterposage" : self.proforma.get_enterposage(),
            "total_lettre" : decimalToText(self.TTC).replace("Dinar", "Dinar(s)") , 
            "paiements" : self.get_paiements(),
        }  
        return context 

    def clean(self):
        if self.id is None :
            records_count = Facture.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Bill aleady exist."})


    def __str__(self):
        return str(self.numero)+" / "+str(self.date_creation.year)

def post_save_facture(sender, instance,**kwargs): 
    try:
        instance.validate_proforma()
        Proforma.objects.filter(article=instance.proforma.article, valide = False, trashed = False).exclude(id=instance.proforma.id).update(trashed = True) 
    except: 
        pass
post_save.connect(post_save_facture, sender = Facture)


class Paiement(models.Model): 
    facture = models.ForeignKey("billing.Facture", on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    banque = models.ForeignKey("reference.Banque", on_delete=models.SET_NULL, null=True,blank=True)
    MODE = [
        ("Chèque","Chèque"), 
        ("Espèce","Espèce"), 
    ]
    mode = models.CharField(choices=MODE, max_length=50)
    cheque = models.CharField(max_length=50,null =True, blank = True)
    montant = DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)

    class Meta:
        verbose_name_plural = "paiements"

def post_save_paiement(sender, instance,**kwargs): 
    facture = instance.facture
    if instance.mode == "Espèce" : 
        facture.add_paiament_espece(Decimal(instance.montant))
    facture.refrech_status()

post_save.connect(post_save_paiement, sender = Paiement)

def post_delete_paiement(sender, instance,**kwargs): 

    try:
        instance.facture.refrech_status() 
    except: 
        pass 
post_delete.connect(post_delete_paiement, sender = Paiement)


class FactureComplementaire(models.Model): 
    
    facture = models.ForeignKey("billing.Facture", on_delete=models.CASCADE)
    numero = models.CharField(max_length=50,blank=True)
    full_number = models.CharField(max_length=50,blank=True)
    date_creation = models.DateField(auto_now_add=True)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    tva = models.BooleanField(default=True) 
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    timber = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    paid = models.BooleanField(default=False, null= False, blank= False)
    history = HistoricalRecords()

    def get_total_lettre(self): 
        return decimalToText(self.TTC).replace("Dinar", "Dinar(s)") 

    def get_lines(self): 
        return self.lignefacturecomplementaire_set.all()

    def get_paiements(self): 
        return self.paiementfacturecomplementaire_set.all()

    def get_total_unpaid_espece(self): 
        total, timber = calculate_timber(self.get_total_unpaid())
        return total

    def get_total_paiments(self): 
        total = self.paiementfacturecomplementaire_set.all().aggregate(total=Sum('montant'))['total']
        if total is None: 
            total = 0
        return total

    def get_total_unpaid(self): 
        try:
            return self.TTC - self.get_total_paiments() 
        except: 
            pass

    def get_total_cheque_paiaments(self): 
        total = self.paiementfacturecomplementaire_set.filter(mode="Chèque").aggregate(total=Sum('montant'))['total']
        if total is None: 
            return 0 
        else: 
            return total 

    def add_paiament_espece(self,montant):
        timber = montant - (self.TTC - self.get_total_cheque_paiaments())
        self.timber = timber 
        ttc = self.TTC + timber 
        self.TTC = ttc


    def calculate_totals(self): 
        total_hors_taxes = 0   
        total_hors_taxes = get_sum_hors_taxes(self.get_lines())
        
        if self.tva and self.facture.proforma.article.client.soumis_tva: 
            total_tva = calculate_tva(total_hors_taxes)
        else:
            total_tva =  0

        self.HT  = total_hors_taxes
        self.TVA  = total_tva 
        self.TTC = total_hors_taxes + total_tva
        self.save()

    def refrech_status(self):
        if self.get_total_paiments() >= self.TTC: 
            self.paid = True 
        else: 
            self.paid = False 
        self.save()


    class Meta:
        verbose_name_plural = "factures complimentaire"

    def save(self, *args, **kwargs):
        list_facture = FactureComplementaire.objects.filter(facture=self.facture).order_by("-id")
        if len(list_facture) <= 0 : 
            numero = 1 
        else: 
            numero = int(list_facture.first().numero) + 1


        self.numero = numero 
        self.full_number = str(self.facture) + " / FC"+ str(numero)

        super(FactureComplementaire, self).save(*args, **kwargs)  

    def __str__(self):
        return str(self.facture)+"/ FC"+str(self.numero)


class LigneFactureComplementaire(models.Model):
    facture_complementaire = models.ForeignKey("billing.FactureComplementaire", on_delete=models.CASCADE)
    rubrique = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False)
    tarif = models.DecimalField(max_digits=15, decimal_places=2)
    quantite = models.IntegerField()
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)


    class Meta:
        verbose_name_plural = "lignes facture complimentaire"

    def save(self, *args, **kwargs):

        self.HT = self.quantite * self.tarif

        if self.facture_complementaire.tva :  
            self.TVA = (self.HT * 19) / 100 
        else:
            self.TVA = 0 

        self.TTC = self.HT + self.TVA  
        super(LigneFactureComplementaire, self).save(*args, **kwargs)  

    def __str__(self):
        return str(self.rubrique)

def post_save_line(sender, instance,**kwargs): 
    try: 
        instance.facture_complementaire.calculate_totals()
    except: 
        pass

post_save.connect(post_save_line, sender = LigneFactureComplementaire)


class PaiementFactureComplementaire(models.Model): 
    facture_complementaire = models.ForeignKey("billing.FactureComplementaire", on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    banque = models.ForeignKey("reference.Banque", on_delete=models.CASCADE, null=True,blank=True)
    MODE = [
        ("Chèque","Chèque"), 
        ("Espèce","Espèce"), 
    ]
    mode = models.CharField(choices=MODE, max_length=50)
    cheque = models.CharField(max_length=50,null =True, blank = True)
    montant = DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)

    class Meta:
        verbose_name_plural = "paiaments facture complimentaire"

def post_save_paiement_complimentaire(sender, instance,**kwargs): 
    facture = instance.facture_complementaire
    if instance.mode == "Espèce" : 
        facture.add_paiament_espece(Decimal(instance.montant))
    facture.refrech_status()

post_save.connect(post_save_paiement_complimentaire, sender = PaiementFactureComplementaire)



class FactureAvoire(models.Model): 
    facture = models.ForeignKey("billing.Facture", on_delete=models.CASCADE)
    numero = models.CharField(max_length=50, blank=True)
    full_number = models.CharField(max_length=50,blank=True)
    date_creation = models.DateField(auto_now_add=True)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    tva = models.BooleanField(default=True) 
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "factures avoire"

    def get_lines(self): 
        return self.lignefactureavoire_set.all()


    def get_total_lettre(self): 
        return decimalToText(self.TTC).replace("Dinar", "Dinar(s)") 

    def calculate_totals(self):

        total_ht = self.lignefactureavoire_set.aggregate(total=Sum('HT'))['total']


        if total_ht == None : 
            total_ht = 0

        preserved_ht = total_ht
        total_ttc = total_ht
        

        if self.tva: 
            total_tax = calculate_tva(total_ht) 
            total_ttc = total_ht + total_tax 
            self.TVA = total_tax

        self.HT = preserved_ht 
        self.TTC = total_ttc

        self.save()
        
    def save(self, *args, **kwargs):
        list_facture = FactureAvoire.objects.filter(facture=self.facture).order_by("-id")
        if len(list_facture) <= 0 : 
            numero = 1 
        else: 
            numero = int(list_facture.first().numero) + 1


        self.numero = numero 
        self.full_number = str(self.facture) + " / FA"+ str(numero)

        super(FactureAvoire, self).save(*args, **kwargs)  

    def __str__(self):
        return str(self.numero)


class LigneFactureAvoire(models.Model):
    facture_avoire= models.ForeignKey("billing.FactureAvoire", on_delete=models.CASCADE)
    rubrique = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False,)
    tarif = models.DecimalField(max_digits=15, decimal_places=2)
    quantite = models.IntegerField()
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)

    class Meta:
        verbose_name_plural = "lignes facture avoire"

    def save(self, *args, **kwargs):
        self.HT = self.quantite * self.tarif

        if self.facture_avoire.tva :  
            self.TVA = (self.HT * 19) / 100 
        else:
            self.TVA = 0 

        self.TTC = self.HT + self.TVA  
        super(LigneFactureAvoire, self).save(*args, **kwargs)  

    def __str__(self):
        return str(self.rubrique)

def post_save_ligne_facture_libre(sender, instance,**kwargs): 
    try:
        instance.facture_avoire.calculate_totals()   
    except: 
        pass 

post_save.connect(post_save_ligne_facture_libre, sender = LigneFactureAvoire)  


class BonSortie(models.Model): 
    numero = models.CharField(max_length=50, default=getNumeroBonSortie)
    date_sortie = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    date_creation = models.DateField(auto_now_add=True)
    facture = models.ForeignKey("billing.Facture", on_delete=models.CASCADE)
    d10 = models.CharField(max_length=50)
    badge = models.CharField(max_length=50)
    history = HistoricalRecords()

    def get_items(self):
        return self.bonsortieitem_set.all()


    def clean(self):
            records_count = BonSortie.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Bon Sortie aleady exist."})

    class Meta:
        verbose_name_plural = "bons de sortie"

    def save(self, *args, **kwargs):

        self.date_sortie = self.facture.proforma.date_proforma 
  
        super(BonSortie, self).save(*args, **kwargs)  

    def __str__(self): 
        return str(self.numero) + str(self.date_creation.year)

class BonSortieItem(models.Model) : 
    bon_sortie = models.ForeignKey("billing.BonSortie", on_delete=models.CASCADE)
    tc  = models.ForeignKey("app.Tc", on_delete=models.CASCADE)
    matricule = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "elements bon de sortie"


class FactureLibre(models.Model): 
    numero = models.CharField(max_length=30,default=getNumeroFactureLibre, verbose_name="numéro de facture")
    client = models.ForeignKey( Client, on_delete=models.SET_NULL, null=True)    
    date_creation = models.DateField(auto_now_add=True)
    date_facture = models.DateField(auto_now=False, auto_now_add=False)
    type_dossier = models.CharField(max_length=200,blank=True, null=True)
    ref = models.CharField(max_length=200, verbose_name="V/Réf",blank=True, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)   
    designation = models.CharField(max_length=200, verbose_name="désignation de marchandises")
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00, verbose_name="hors taxes")
    tva = models.BooleanField(default=True, verbose_name="") 
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00, verbose_name="toutes taxes comproses")
    timber = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0.00)
    remise = models.BooleanField(default=False)
    REMISE = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
    TR = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
    paid = models.BooleanField(default=False, null= False, blank= False)
    history = HistoricalRecords()   

    def get_lines(self): 
        return self.lignefacturelibre_set.all()

    def get_paiements(self): 
        return self.paiementfacturelibre_set.all()


    def get_total_paiments(self): 
        return self.paiementfacturelibre_set.all().aggregate(total=Sum('montant'))['total']


    def get_total_cheque_paiaments(self): 
        total = self.paiementfacturelibre_set.filter(mode="Chèque").aggregate(total=Sum('montant'))['total']
        if total is None: 
            return 0 
        else: 
            return total 

    def add_paiament_espece(self,montant):
        timber = montant - (self.TTC - self.get_total_cheque_paiaments())
        self.timber = timber 
        ttc = self.TTC + timber 
        self.TTC = ttc

    @property
    def unpaid_espece(self): 
        total, timber = calculate_timber(self.unpaid)
        return total

    @property 
    def unpaid(self): 
        return self.TTC - self.total_paid 

    @property 
    def total_paid(self): 
        total = self.get_total_paiments()
        if total is None: 
            total = 0
        return total


    def refrech_status(self):
        if self.get_total_paiments() >= self.TTC: 
            self.paid = True 
        else: 
            self.paid = False 
        self.save()



    def get_billing_info(self):
        context = {
            "facture" : self,
            "lignes_prestations" : self.lignefacturelibre_set.all(),
            "total_lettre" : decimalToText(self.TTC).replace("Dinar", "Dinar(s)") , 
            "paiements" : self.paiementfacturelibre_set.all(),
        }  
        return context 
        

    def calculate_totals(self):

        total_ht = self.lignefacturelibre_set.aggregate(total=Sum('HT'))['total']


        if total_ht == None : 
            total_ht = 0

        preserved_ht = total_ht
        total_ttc = total_ht
        
        if self.remise: 
            total_ht,total_remise = calculate_remise(total_ht,self.REMISE)
            self.TR = total_remise

        if self.tva: 
            total_tax = calculate_tva(total_ht) 
            total_ttc = total_ht + total_tax 
            self.TVA = total_tax

        self.HT = preserved_ht 
        self.TTC = total_ttc

        self.save()

    def get_paiement_info():
        pass

    def save(self, *args, **kwargs):
        if(self.client.soumis_tva is False): 
            self.tva = False 
        super(FactureLibre, self).save(*args, **kwargs)  

    class Meta:
        ordering = ["-numero"]
        verbose_name_plural = "factures libre"

    def __str__(self):
        return str(self.numero)+" / "+str(self.date_creation.year)


class LigneFactureLibre(models.Model):
    facture_libre = models.ForeignKey("billing.FactureLibre", on_delete=models.CASCADE)
    rubrique = models.ForeignKey("bareme.Rubrique", on_delete=models.CASCADE)
    tarif = models.DecimalField(max_digits=15, decimal_places=2)
    quantite = models.IntegerField()
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)

    class Meta:
        verbose_name_plural = "lignes facture libre"

    def save(self, *args, **kwargs):

        self.HT = self.quantite * self.tarif

        
        if self.facture_libre.tva :  
            self.TVA = (self.HT * 19) / 100 
        else:
            self.TVA = 0 
            
        self.TTC = self.HT + self.TVA 
        
        super(LigneFactureLibre, self).save(*args, **kwargs)   


    def __str__(self):
        return str(self.rubrique)

        
def post_save_ligne_facture_libre(sender, instance,**kwargs): 
    try:
        instance.facture_libre.calculate_totals()   
    except: 
        pass 

post_save.connect(post_save_ligne_facture_libre, sender = LigneFactureLibre)  


def post_delete_ligne_facture_libre(sender, instance,**kwargs): 
    try:
        instance.facture_libre.calculate_totals()   
    except: 
        pass 
post_delete.connect(post_delete_ligne_facture_libre, sender = LigneFactureLibre)


class PaiementFactureLibre(models.Model): 
    facture_libre = models.ForeignKey("billing.FactureLibre", on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    banque = models.ForeignKey("reference.Banque", on_delete=models.CASCADE, null=True,blank=True)
    MODE = [
        ("Chèque","Chèque"), 
        ("Espèce","Espèce"), 
    ]
    mode = models.CharField(choices=MODE, max_length=50)
    cheque = models.CharField(max_length=50,null =True, blank = True)
    montant = DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)

    class Meta:
        verbose_name_plural = "paiaments facture libre"


def post_save_paiement_libre(sender, instance,**kwargs): 
    facture = instance.facture_libre
    if instance.mode == "Espèce" : 

        facture.add_paiament_espece(instance.montant)
    facture.refrech_status()

post_save.connect(post_save_paiement_libre, sender = PaiementFactureLibre)


class ProformaGroupage(models.Model): 
    gros = models.ForeignKey("app.Gros", on_delete=models.CASCADE)
    article = models.ForeignKey("app.Article", on_delete=models.CASCADE)
    sous_article = models.ForeignKey("app.SousArticle", on_delete=models.CASCADE)
    numero = models.CharField(max_length=12,default=getNumeroProformaGroupage)
    date_creation = models.DateField(auto_now_add=True)
    date_proforma = models.DateField(auto_now=False, auto_now_add=False, null = True)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    debeur = models.BooleanField(default=False, verbose_name="DEBEUR")
    DEBEUR = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    tva = models.BooleanField(default=True, verbose_name="TVA") 
    remise = models.BooleanField(default=False)
    REMISE = models.DecimalField(max_digits=15, decimal_places=2,default=0,blank=True, null=True)
    TR = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    valide = models.BooleanField(default=False, blank=True, null=True)
    trashed = models.BooleanField(default=False, blank=True, null=True)
    enterposage = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "proformas groupage"

    def get_prestations(self):
        return self.ligneproformagroupage_set.all()

    def get_ttc_in_letters(self): 
        return decimalToText(self.TTC)
    
    def calculate_totals(self): 
        total_hors_taxes = 0   
        total_hors_taxes = get_sum_hors_taxes(self.get_prestations())
        remise = 0     
        if self.remise: 
            total_hors_taxes,remise = calculate_remise(total_hors_taxes, self.REMISE)
        

        if self.tva: 
            total_tva = calculate_tva(total_hors_taxes) 
        else: 
            total_tva =  0  

        self.HT  = total_hors_taxes
        self.TVA  = total_tva 
        self.TR = remise
        self.TTC = total_hors_taxes + total_tva
        if self.debeur: 
            self.TTC += self.DEBEUR
        self.save()
        
    def validate(self):
        self.valide = True 
        self.save()
              
    def clean(self):
        if self.id is None :
            records_count = ProformaGroupage.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Bill aleady exist."})

    def __str__(self):
        return str(self.numero)+" / "+str(self.date_creation.year)  

import decimal                 
class LigneProformaGroupage(models.Model): 
    proforma = models.ForeignKey("billing.ProformaGroupage",on_delete=models.CASCADE) 
    rubrique = models.CharField(max_length=100)
    quantite = models.DecimalField(max_digits=15, decimal_places=2,blank=True , null= True)
    tarif = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    rubrique_object = models.ForeignKey("bareme.Rubrique", on_delete=models.PROTECT, null=True, blank=True)
    code_comptable = models.CharField(max_length=30, null=True, blank=True) 
   
    def update_tva_zero(self): 
        self.TVA = 0 
        self.TTC = self.HT 
        self.save()
        
    class Meta:
        verbose_name_plural = "lignes prestation"

    def save(self, *args, **kwargs):
        
        if self.proforma.tva: 
            self.HT = self.tarif * decimal.Decimal(self.quantite)
            self.TVA = (self.HT * 19) / 100
            self.TTC = self.HT + self.TVA
            
        else: 
            self.HT = self.tarif * decimal.Decimal(self.quantite)
            self.TVA = 0
            self.TTC = self.tarif * decimal.Decimal(self.quantite)     
                
        super(LigneProformaGroupage, self).save(*args, **kwargs)   

    def __str__(self):
        return self.rubrique 
    
class FactureGroupage(models.Model): 
    proforma = models.ForeignKey("billing.ProformaGroupage", on_delete=models.CASCADE, null=True)    
    numero = models.CharField(max_length=12,default=getNumeroFactureGroupage)
    date_creation = models.DateField(auto_now_add=True)
    HT = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TVA = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TTC = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    TR = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    DEBEUR = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    timber = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True,default=0)
    paid = models.BooleanField(default=False, null= False, blank= False)
    a_terme  = models.BooleanField(default=False, null= False, blank= False)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "factures groupage"

    def validate_proforma(self): 
        self.HT = self.proforma.HT
        self.TVA = self.proforma.TVA
        self.TR = self.proforma.TR
        self.TTC = self.proforma.TTC
        self.DEBEUR = self.proforma.DEBEUR 
        self.save()
        self.proforma.validate()

    def get_paiements(self): 
        return self.paiementsgroupage_set.all()

    def get_total_paiments(self): 
        return self.paiementgroupage_set.all().aggregate(total=Sum('montant'))['total']

    def get_total_cheque_paiaments(self): 
        total = self.paiementgroupage_set.filter(mode="Chèque").aggregate(total=Sum('montant'))['total']
        if total is None: 
            return 0 
        else: 
            return total 

    def get_paiements(self): 
        return self.paiementgroupage_set.all()

    def pay_a_terme(self) : 
        self.a_terme = True
        self.save()

    def refrech_status(self):
        if self.get_total_paiments() >= self.proforma.TTC: 
            self.paid = True 
        else: 
            self.paid = False 
        self.save()
    
    def add_paiament_espece(self,montant):
        
        timber = montant - (self.TTC - self.get_total_cheque_paiaments())
        
        self.timber = timber 
        ttc = self.TTC + timber 
        self.TTC = ttc
        self.save()
        
    def get_factrue_lines(self): 
        prestations = self.proforma.ligneproformagroupage_set.values('proforma','rubrique','rubrique_object','rubrique_object__direction__code','tarif','HT','TVA','TTC',"code_comptable")
        return prestations
    
    @property
    def unpaid_espece(self): 
        total, timber = calculate_timber(self.unpaid)
        return total

    @property 
    def unpaid(self): 
        try:
            return self.TTC - self.total_paid 
        except: 
            pass
        
    @property 
    def total_paid(self): 
        total = self.get_total_paiments()
        if total is None: 
            total = 0
        return total
    @property 
    def facture_number(self): 
        return str(self.numero)+"/"+str(self.proforma.date_proforma.year) 

    @property
    def client(self): 
        return self.proforma.sous_article.client.raison_sociale+" G-"+str(self.proforma.gros.numero)+" A-"+str(self.proforma.article.numero) + " SA-"+str(self.proforma.sous_article.numero)
                
    def clean(self):
        if self.id is None :
            records_count = FactureGroupage.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Bill aleady exist."})

    def __str__(self):
        return str(self.numero)+" / "+str(self.date_creation.year)

def post_save_facture_groupage(sender, instance,**kwargs): 
    try:
        if instance.TTC is None: 
            instance.validate_proforma()
            ProformaGroupage.objects.filter(article=instance.proforma.article,sous_article=instance.proforma.sous_article, valide = False, trashed = False).exclude(id=instance.proforma.id).update(trashed = True) 
    except: 
        pass
post_save.connect(post_save_facture_groupage, sender = FactureGroupage)

class PaiementGroupage(models.Model): 
    facture = models.ForeignKey("billing.FactureGroupage", on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    banque = models.ForeignKey("reference.Banque", on_delete=models.SET_NULL, null=True,blank=True)
    MODE = [
        ("Chèque","Chèque"), 
        ("Espèce","Espèce"), 
    ]
    mode = models.CharField(choices=MODE, max_length=50)
    cheque = models.CharField(max_length=50,null =True, blank = True)
    montant = DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)

    class Meta:
        verbose_name_plural = "paiements groupage"

def post_save_paiement_groupage(sender, instance,**kwargs): 
    facture = instance.facture
    if instance.mode == "Espèce" : 
        facture.add_paiament_espece(Decimal(instance.montant))
    facture.refrech_status()

post_save.connect(post_save_paiement_groupage, sender = PaiementGroupage)


class BonSortieGroupage(models.Model): 
    numero = models.CharField(max_length=50, default=getNumeroBonSortieGroupage)
    date_sortie = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    sous_article = models.ForeignKey("app.SousArticle", on_delete=models.CASCADE)
    date_creation = models.DateField(auto_now_add=True)
    facture = models.ForeignKey("billing.FactureGroupage", on_delete=models.CASCADE)
    d10 = models.CharField(max_length=50)
    badge = models.CharField(max_length=50)
    matricule = models.CharField(max_length=50)
    history = HistoricalRecords()


    def clean(self):
            records_count = BonSortieGroupage.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Bon Sortie aleady exist."})

    class Meta:
        verbose_name_plural = "bons de sortie groupage"

    def save(self, *args, **kwargs):

        self.date_sortie = self.facture.proforma.date_proforma 
  
        super(BonSortieGroupage, self).save(*args, **kwargs)  

    def __str__(self): 
        return str(self.numero) + str(self.date_creation.year)
